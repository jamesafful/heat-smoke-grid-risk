#!/usr/bin/env python
import argparse, pandas as pd, pathlib, numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", required=True)
    ap.add_argument("--out", default="paper/tables/table1_pilot_summary.csv")
    args = ap.parse_args()

    df = pd.read_parquet(args.panel)
    # simple summary by county
    g = df.groupby("fips").agg(
        n_days=("date","nunique"),
        pm25_mean=("pm25_mean","mean"),
        pm25_p95=("pm25_mean",lambda s: np.percentile(s,95)),
        smoke_light_mean=("share_light","mean"),
        smoke_heavy_mean=("share_heavy","mean"),
        outage_days=("event_any","sum"),
        peak_out_max=("cust_out_peak","max")
    ).reset_index()
    outp = pathlib.Path(args.out); outp.parent.mkdir(parents=True, exist_ok=True)
    g.to_csv(outp, index=False)
    print(f"Wrote {outp}")

if __name__ == "__main__":
    main()
