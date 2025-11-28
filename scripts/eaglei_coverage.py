#!/usr/bin/env python
import argparse, duckdb, pandas as pd, pathlib

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", default="data/raw/eaglei/*.csv", help="glob of EAGLE-I CSVs")
    ap.add_argument("--out", default="paper/tables/eaglei_coverage.csv", help="output CSV")
    args = ap.parse_args()

    con = duckdb.connect()
    q = f"""
    SELECT 
      CAST(fips_code AS VARCHAR) AS fips,
      MIN(run_start_time) AS min_ts,
      MAX(run_start_time) AS max_ts,
      COUNT(*) AS n_rows
    FROM read_csv_auto('{args.glob}', header=True)
    GROUP BY fips_code
    ORDER BY fips
    """
    df = con.sql(q).df()
    outp = pathlib.Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(outp, index=False)
    print(f"Wrote {outp} with {len(df)} counties")

if __name__ == "__main__":
    main()
