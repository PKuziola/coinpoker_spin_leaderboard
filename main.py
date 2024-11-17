import calendar
import os
import re
import time
from datetime import date, timedelta

import pandas as pd
import pandas_gbq
from dotenv import load_dotenv

from google.cloud import bigquery
from google.oauth2 import service_account

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

url = "https://coinpoker.com/promotions/daily-cosmic-spins-leaderboard/"

options = webdriver.ChromeOptions()
options.add_argument("--headless=true")


def text(e):
    if not (r := e.text):
        r = e.get_attribute("textContent")
    return r.strip() if r else ""


with webdriver.Chrome(options) as driver:
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    buttons = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "button[aria-selected='false']")
        )
    )

    yesterday_buttons = [button for button in buttons if text(button) == "Yesterday"]

    first_button = yesterday_buttons[0]
    second_button = yesterday_buttons[1]

    driver.execute_script("arguments[0].click();", first_button)
    driver.execute_script("arguments[0].click();", second_button)
    time.sleep(3)

    body_text = driver.find_element(By.TAG_NAME, "body").text

    start = body_text.index("$0.25, $1, $3 and $5 Leaderboard")
    end = body_text.index(
        "Please carefully read the terms and conditions to ensure your eligibility for this promotion."
    )

    raw_string = body_text[start:end]

    divide_lb_str_loc = raw_string.index("$10, $25, $50 and $100 Leaderboard")

    low_stakes_lb_string = raw_string[:divide_lb_str_loc]
    high_stakes_lb_string = raw_string[divide_lb_str_loc:]

    low_lines = low_stakes_lb_string.splitlines()
    high_lines = high_stakes_lb_string.splitlines()

    columns = [
        "date",
        "weekday",
        "is_weekend",
        "lb_type",
        "place",
        "player",
        "points",
        "prize",
        "spins_to_play_5s",
        "spins_to_play_10s",
        "estimated_rakeback",
    ]
    df = pd.DataFrame(columns=columns)

    today = date.today()
    yesterday = today - timedelta(1)
    yesterday_weekday = yesterday.weekday()
    yesterday_name = calendar.day_name[yesterday_weekday]

    if yesterday_name not in ["Friday", "Saturday", "Sunday"]:
        is_weekend = 0
    is_weekend = 1

    avg_points_per_spin_5s = 15
    avg_points_per_spin_10s = 30

    rake_5s = 0.05 * 5
    rake_10s = 0.05 * 10

    # low_leaderboard
    for line in low_lines[4:-1]:
        temp_list = line.split()

        points = float(temp_list[2].replace(",", ""))

        if len(temp_list) > 4:
            integers = re.findall(r"\d+", temp_list[5])
            prize = int("".join(integers)) * int(temp_list[3])
        else:
            prize = 0

        new_row = {
            "date": yesterday,
            "weekday": yesterday_name,
            "is_weekend": is_weekend,
            "lb_type": "low",
            "place": int(temp_list[0]),
            "player": temp_list[1],
            "points": points,
            "prize": prize,
            "spins_to_play_5s": int((points // avg_points_per_spin_5s) + 1),
            "spins_to_play_10s": None,
            "estimated_rakeback": round(
                (prize) / (((points // avg_points_per_spin_5s) + 1) * rake_5s) * 100, 2
            ),
        }
        df.loc[len(df)] = new_row

    # high_leaderboard
    for line in high_lines[4:]:
        temp_list = line.split()

        points = float(temp_list[2].replace(",", ""))

        if len(temp_list) > 4:
            integers = re.findall(r"\d+", temp_list[5])
            prize = int("".join(integers)) * int(temp_list[3])
        else:
            prize = 0

        new_row = {
            "date": yesterday,
            "weekday": yesterday_name,
            "is_weekend": is_weekend,
            "lb_type": "high",
            "place": int(temp_list[0]),
            "player": temp_list[1],
            "points": points,
            "prize": prize,
            "spins_to_play_5s": None,
            "spins_to_play_10s": int((points // avg_points_per_spin_10s) + 1),
            "estimated_rakeback": round(
                (prize) / (((points // avg_points_per_spin_10s) + 1) * rake_10s) * 100,
                2,
            ),
        }
        df.loc[len(df)] = new_row

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    credentials = service_account.Credentials.from_service_account_file(
        f"{os.environ.get('GOOGLE_CLOUD_JSON_KEY_FILE')}",
        scopes=["https://www.googleapis.com/auth/bigquery"],
    )

    df["spins_to_play_5s"] = df["spins_to_play_5s"].astype("Int64")
    df["spins_to_play_10s"] = df["spins_to_play_10s"].astype("Int64")

    client = bigquery.Client(
        credentials=credentials,
        project=credentials.project_id,
    )

    pandas_gbq.to_gbq(
        df,
        f"{credentials.project_id}.coinpoker_data.lb_table",
        project_id=credentials.project_id,
        if_exists="append",
        location="US",
        credentials=credentials,
    )
