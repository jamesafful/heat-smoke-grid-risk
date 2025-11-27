import argparse
import pandas as pd
from pathlib import Path
from ..data_paths import OUTPUTS, DATA_SAMPLE
from .fetch_epa_pm25 import load_sample_pm25
from .fetch_hms_smoke import load_sample_hms
from .fetch_eagle_outages import load_sample_outages

def build_sample_panel():
    pm = load_sample_pm25().rename(columns={"date_local":"date"})
    smoke = load_sample_hms()
    out = load_sample_outages().assign(date=lambda d: d["run_start_time"].dt.date)
    out["date"] = pd.to_datetime(out["date"])
    # aggregate outages to daily (peak customers out per day as example metric)
    daily_out = (out.groupby(["fips_code","date"], as_index=False)["customers_out"]
                   .max().rename(columns={"customers_out":"cust_out_peak"}))
    # merge on a chosen date present in samples (2020-09-09 vs outages 2018-09-14 will not overlap)
    # For demo, just produce separate artifacts and a small merged panel by fake align (same county different dates)
    pm_small = pm.head(10)
    smoke_small = smoke.head(10)
    merged = daily_out.head(10)
    # save
    OUTPUTS.mkdir(exist_ok=True, parents=True)
    pm_small.to_parquet(OUTPUTS / "pm25_sample.parquet")
    smoke_small.to_parquet(OUTPUTS / "hms_smoke_sample.parquet")
    merged.to_parquet(OUTPUTS / "outages_sample.parquet")
    return {"pm25_rows": len(pm_small), "smoke_rows": len(smoke_small), "outage_rows": len(merged)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true", help="run sample build")
    args = ap.parse_args()
    if args.sample:
        stats = build_sample_panel()
        print(stats)

if __name__ == "__main__":
    main()
