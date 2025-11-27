import os, pandas as pd
from pathlib import Path
from ..data_paths import DATA, DATA_SAMPLE

def load_sample_pm25():
    return pd.read_csv(DATA_SAMPLE / "pm25_cook_2019_2020.csv", parse_dates=["date_local"])

def fetch_real_pm25(years=(2019,2020), state_code="17", county_code="031"):
    # Placeholder: show URLs and return empty DF if offline
    # Real EPA pre-generated files: daily_88101_YYYY.zip
    urls = [f"https://aqs.epa.gov/airdata/daily_88101_{y}.zip" for y in years]
    return urls  # user fetch step documented in README
