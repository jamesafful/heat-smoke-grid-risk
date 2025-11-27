import pandas as pd
from pathlib import Path
from ..data_paths import DATA_SAMPLE

def load_sample_outages():
    df = pd.read_csv(DATA_SAMPLE / "outages_2018-09-14_sample.csv", parse_dates=["run_start_time"])
    return df

def data_descriptor_ref():
    return "https://www.nature.com/articles/s41597-024-03095-5"
