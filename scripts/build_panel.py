#!/usr/bin/env python
import argparse, pathlib, pandas as pd, duckdb, os

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True, help="5-digit FIPS, e.g., 17031")
    ap.add_argument("--start", required=True, type=pd.to_datetime)
    ap.add_argument("--end", required=True, type=pd.to_datetime)
    ap.add_argument("--pm", required=True, help="path to pm25 parquet from ingest_pm25.py")
    ap.add_argument("--smoke", required=True, help="path to smoke parquet from smoke_intersect.py")
    ap.add_argument("--eaglei-csv", default="", help="path to eaglei_outages_YEAR.csv (optional)")
    ap.add_argument("--out", required=True, help="panel parquet path")
    args = ap.parse_args()

    fips = str(args.county).zfill(5)
    start, end = args.start.normalize(), args.end.normalize()

    # --- PM ---
    pm = pd.read_parquet(args.pm)
    pm["date"] = pd.to_datetime(pm["date"])
    # Ensure full coverage of the requested window and attach fips
    idx = pd.DataFrame({"date": pd.date_range(start, end)})
    pm = idx.merge(pm, on="date", how="left")
    pm["fips"] = fips

    # --- Smoke ---
    smk = pd.read_parquet(args.smoke)
    smk["date"] = pd.to_datetime(smk["date"])
    smk["fips"] = smk["fips"].astype(str).str.zfill(5)

    # --- Outages (optional) ---
    out_daily = pd.DataFrame({
        "fips": [fips]*len(idx),
        "date": idx["date"],
        "cust_out_peak": 0,
        "cust_out_sum": 0,
        "total_customers": pd.NA
    })

    # NOTE: argparse uses underscores for attribute names
    if args.eaglei_csv and os.path.exists(args.eaglei_csv):
        con = duckdb.connect()
        q = """
        SELECT fips_code, run_start_time, customers_out, total_customers
        FROM read_csv_auto(?, header=True)
        WHERE fips_code = ?
          AND run_start_time >= TIMESTAMP ?
          AND run_start_time <  TIMESTAMP ?
        """
        df = con.execute(
            q,
            [args.eaglei_csv, int(fips), str(start.date()), str((end + pd.Timedelta(days=1)).date())]
        ).df()

        if not df.empty:
            df["date"] = pd.to_datetime(df["run_start_time"]).dt.floor("D")
            grp = (df.groupby("date", as_index=False)
                     .agg(cust_out_peak=("customers_out","max"),
                          cust_out_sum=("customers_out","sum"),
                          total_customers=("total_customers","max")))
            grp["fips"] = fips
            out_daily = idx.merge(grp, on="date", how="left")
            out_daily["fips"] = fips
            out_daily["cust_out_peak"] = out_daily["cust_out_peak"].fillna(0).astype(int)
            out_daily["cust_out_sum"]  = out_daily["cust_out_sum"].fillna(0).astype(int)
            if out_daily["total_customers"].notna().any():
                out_daily["total_customers"] = out_daily["total_customers"].fillna(out_daily["total_customers"].max()).astype(int)
            else:
                out_daily["total_customers"] = 0

    # --- Merge panel (on fips+date everywhere) ---
    panel = (pm.merge(smk, on=["fips","date"], how="left")
               .merge(out_daily, on=["fips","date"], how="left"))

    for c in ["share_light","share_moderate","share_heavy"]:
        panel[c] = panel.get(c, 0).fillna(0.0)

    panel["cust_out_peak"] = panel["cust_out_peak"].fillna(0).astype(int)
    panel["cust_out_sum"]  = panel["cust_out_sum"].fillna(0).astype(int)
    panel["total_customers"] = panel["total_customers"].fillna(0).astype(int)
    panel["event_any"] = (panel["cust_out_peak"] > 0).astype(int)

    cols = ["fips","date","pm25_mean","share_light","share_moderate","share_heavy",
            "cust_out_peak","cust_out_sum","total_customers","event_any"]
    panel = panel[cols].sort_values("date")

    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(out_path, index=False)
    panel.to_csv(out_path.with_suffix(".csv"), index=False)
    print(f"Wrote panel: {out_path} and {out_path.with_suffix('.csv')}")

if __name__ == "__main__":
    main()
