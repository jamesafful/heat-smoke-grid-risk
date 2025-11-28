#!/usr/bin/env python
import argparse, pandas as pd, pathlib

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", nargs="+", required=True, help="panel parquet paths")
    ap.add_argument("--out", required=True, help="output parquet")
    args = ap.parse_args()

    dfs = []
    for p in args.inputs:
        df = pd.read_parquet(p)
        dfs.append(df)
    out = pd.concat(dfs, ignore_index=True).sort_values(["fips","date"])
    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(out_path, index=False)
    print(f"Wrote {out_path} with {len(out)} rows, {out['fips'].nunique()} counties")

if __name__ == "__main__":
    main()
