import pandas as pd
from pathlib import Path
from ..data_paths import DATA_SAMPLE

def load_sample_hms():
    return pd.read_csv(DATA_SAMPLE / "hms_smoke_2020-09-09.csv", parse_dates=["date"])

def hms_docs_url():
    return "https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/Shapefile/"
