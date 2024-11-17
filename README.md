<a name="readme-top"></a>
# 📚 Table of Contents
- [ℹ About The Project](#about) 
- [🛢Database](#db)
- [🔑Setup](#setup)
- [📊 Apache Superset Visualization](#viz)
- [🌲 Project tree](#tree)
- [📄 License](#license)



<a name="about"></a>
<!-- ABOUT THE PROJECT -->
# ℹ️ About The Project


<img src="https://www.techopedia.com/wp-content/uploads/2024/04/feat-img-coinpoker.svg" width="400" height="227.5" />

This Python-based project is designed to scrape, process, and store data from the [CoinPoker Cosmic Spins Leaderboard](https://coinpoker.com/promotions/daily-cosmic-spins-leaderboard/#termsContent), which showcases player performance in daily promotional spin-based competitions. <br>The script gathers leaderboard data, calculates necessary metrics, estimates rakeback, and uploads the processed results to Google BigQuery for further analysis.<br>
Due to dynamic webpage elements Selenium was used.

## Additional information:
- Calculations are focused on 5s and 10s spins.
- Rakeback is paid in CHP tokens.
- Calculations assume that player always finish second.
- The leaderboard results assume a strategy of prioritizing 5s spins for the low leaderboard and 10s spins for the high leaderboard.

## 👨‍💻 Built with

| Technology                                                                                                  | Usage                             |
|-------------------------------------------------------------------------------------------------------------|-----------------------------------|
| <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>       | Scraping                         |
| <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white" />    | Handling data                    |
| <img src="https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" /> | Scalability, performance, cost-effectiveness |
| <img src="https://cdn-glbkn.nitrocdn.com/nueVERAekgEhYIWQHKPLZSnFYDdYisoI/assets/images/optimized/rev-2e6d147/syncari.com/wp-content/uploads/2021/03/Google-Big-Query.png" width="100" height="27,5"/> | Data storage                     |
| <img src="https://www.itop.es/images/Tecnologias/superset-logo-itop.png" width="100" height="27,5"/>        | Data visualization               |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="db"></a>
# 🛢Database information

|  column name |  type |  description | 
|---|---|---|
| date  |  TIMESTAMP |  Timestamp of the leaderboard entry, indicating when the data was recorded. |
|  weekday | STRING  | Day of the week corresponding to the date, e.g., "Monday" or "Friday."  |
|  is_weekend | INTEGER  | 	Indicator of whether the date falls on a weekend (1 for yes, 0 for no, we treat friday as weekend).  |
|  lb_type | STRING  | The type of leaderboard (low or high).  |
|  place | INTEGER  | Position of the player on the leaderboard.  |
|  player | STRING  | Username of the player participating in the leaderboard.  |
|  points | FLOAT  |  	Points earned by the player in the daily leaderboard. |
|  prize |  INTEGER |  Prize amount awarded to the player for their performance. |
|  spins_to_play_5s | INTEGER  | Number of 5s spin games to play to achieve the same amount of points.  |
|  spins_to_play_10s | INTEGER | Number of 10s spin games to play to achieve the same amount of points.   |
|  estimated_rakeback | FLOAT  |  Estimated rakeback amount the player will receive based on their performance. |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="setup"></a>
# 🔑Setup 

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Getting Started
```bash
# Clone the repository
$ git clone https://github.com/PKuziola/coinpoker_spin_leaderboard.git
# Navigate to the project folder
$ cd coinpoker_spin_leaderboard
# Remove the original remote repository
$ git remote remove origin
# Create the virtual environment
$ python -m venv env
# Activate the virtual environment
# On Windows
$ env\Scripts\activate
# On macOS/Linux
$ source env/bin/activate
```
## Google Cloud Platform setup

Create service account with following permissions:
```
- roles/bigquery.dataEditor
- roles/bigquery.user
```
Commands to create service account and grant permissions, alternatively you can also do it using the Google Cloud web interface, Instruction in resources.
```
gcloud iam service-accounts create [SERVICE_ACCOUNT_NAME] --description="[DESCRIPTION]" --display-name="[DISPLAY_NAME]"
gcloud projects add-iam-policy-binding [PROJECT_ID] --member=serviceAccount:[SERVICE_ACCOUNT_EMAIL] --role=roles/bigquery.dataEditor
gcloud projects add-iam-policy-binding [PROJECT_ID] --member=serviceAccount:[SERVICE_ACCOUNT_EMAIL] --role=roles/bigquery.user
```

Remember to:
- download service account key as .json file and put it into directory
- create dataset in Google Big Query database

In case you used different names than mine do code adjustments.

## Resources
- [Google Cloud service accounts official Documentaion](https://cloud.google.com/iam/docs/service-accounts-create#gcloud)
- [Google Cloud Manage access to service accounts official Documentaion](https://cloud.google.com/iam/docs/manage-access-service-accounts#iam-view-access-sa-gcloud)
- [How to create service account and get JSON file key](https://docs.edna.io/kb/get-service-json#account)

## Running project
```
$ python3 main.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="viz"></a>
# 📊 Apache Superset Visualization

To Be Done

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="tree"></a>
# 🌲 Project tree
```bash
.
├─── .env-sample
├─── .gitignore
├─── CHANGELOG.md
├─── google_cloud_service_account_key.json #Google Cloud service account .json key
├─── license.txt
├─── main.py #Main script for scraping and processing data
├─── README.md
└─── requirements.txt #Lists Python dependencies
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="license"></a>
# 📄 License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


