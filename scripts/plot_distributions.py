#!/usr/bin/env python
import argparse, pandas as pd, pathlib, matplotlib.pyplot as plt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", required=True)
    ap.add_argument("--out", default="paper/figures/panel_distributions.png")
    args = ap.parse_args()

    df = pd.read_parquet(args.panel)
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    df["pm25_mean"].plot(kind="hist", bins=15, alpha=0.6)
    ax.set_xlabel("PM2.5 (µg/m³)")
    ax.set_ylabel("Count of county-days")
    ax.set_title("Distribution of PM2.5 across pilot county-days")
    pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout(); plt.savefig(args.out, dpi=200)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
