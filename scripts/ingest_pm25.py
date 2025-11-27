#!/usr/bin/env python
import argparse, pathlib, pandas as pd

def years_in_range(start, end):
    ys = set([start.year, end.year])
    return sorted(ys)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True, help="5-digit FIPS, e.g., 17031")
    ap.add_argument("--start", required=True, type=pd.to_datetime)
    ap.add_argument("--end", required=True, type=pd.to_datetime)
    ap.add_argument("--epa-dir", default="data/raw/epa")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    county = args.county.zfill(5)
    state_code, county_code = county[:2], county[2:]
    start, end = args.start.normalize(), args.end.normalize()

    usecols = ["State Code","County Code","Site Num","Date Local","Arithmetic Mean"]
    frames = []
    for y in years_in_range(start, end):
        csv = pathlib.Path(args.epa_dir)/f"daily_88101_{y}.csv"
        if not csv.exists():
            raise FileNotFoundError(f"Missing EPA file: {csv}")
        df = pd.read_csv(csv, usecols=usecols,
                         dtype={"State Code":str,"County Code":str,"Site Num":str})
        df = df[(df["State Code"]==state_code) & (df["County Code"]==county_code)].copy()
        if df.empty: 
            continue
        df["date"] = pd.to_datetime(df["Date Local"])
        frames.append(df[["date","Arithmetic Mean"]])

    if frames:
        pm = pd.concat(frames, ignore_index=True)
        pm = pm[(pm["date"]>=start)&(pm["date"]<=end)]
        pm_day = (pm.groupby("date", as_index=False)["Arithmetic Mean"]
                    .mean().rename(columns={"Arithmetic Mean":"pm25_mean"}))
    else:
        # no monitors -> empty set
        pm_day = pd.DataFrame({"date": pd.date_range(start, end), "pm25_mean": pd.NA})

    pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    pm_day.to_parquet(args.out, index=False)
    print(f"Wrote {args.out} with {len(pm_day)} rows")

if __name__ == "__main__":
    main()
