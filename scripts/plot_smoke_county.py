#!/usr/bin/env python
import argparse, geopandas as gpd, pandas as pd, pathlib, matplotlib.pyplot as plt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True, help="FIPS, e.g. 17031")
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--hms-dir", default="data/raw/hms")
    ap.add_argument("--counties-shp", default="data/raw/counties/cb_2020_us_county_500k.shp")
    ap.add_argument("--out", default="paper/figures/smoke_map.png")
    args = ap.parse_args()

    y, m, d = args.date.split("-")
    shp = pathlib.Path(args.hms_dir)/y/m/f"hms_smoke{y}{m}{d}.shp"
    counties = gpd.read_file(args.counties_shp).to_crs(3857)
    cook = counties[counties["GEOID"]==args.county].to_crs(3857)
    smoke = gpd.read_file(shp).to_crs(3857)

    # Plot
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111)
    cook.boundary.plot(ax=ax, linewidth=1)
    if len(smoke):
        smoke.plot(ax=ax, alpha=0.3, linewidth=0.2)
    ax.set_axis_off()
    plt.tight_layout()
    outp = pathlib.Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(outp, dpi=200)
    print(f"Wrote {outp}")

if __name__ == "__main__":
    main()
