#!/usr/bin/env python
import argparse, pathlib, pandas as pd, geopandas as gpd

def daterange(start, end):
    d = pd.to_datetime(start)
    end = pd.to_datetime(end)
    while d <= end:
        yield d
        d = d + pd.Timedelta(days=1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True, help="5-digit FIPS, e.g., 17031")
    ap.add_argument("--start", required=True, type=pd.to_datetime)
    ap.add_argument("--end", required=True, type=pd.to_datetime)
    ap.add_argument("--hms-dir", default="data/raw/hms")
    ap.add_argument("--counties-shp", default="data/raw/counties/cb_2020_us_county_500k.shp")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    fips = args.county.zfill(5)
    start, end = args.start.normalize(), args.end.normalize()

    # County geometry
    cty = gpd.read_file(args.counties_shp)
    if "GEOID" in cty.columns:
        cty["GEOID"] = cty["GEOID"].astype(str).str.zfill(5)
        cook = cty[cty["GEOID"]==fips][["GEOID","geometry"]].rename(columns={"GEOID":"fips"})
    else:
        # fallback on STATEFP+COUNTYFP
        cty["fips"] = (cty["STATEFP"].astype(str)+cty["COUNTYFP"].astype(str)).str.zfill(5)
        cook = cty[cty["fips"]==fips][["fips","geometry"]]
    if cook.empty:
        raise ValueError(f"FIPS {fips} not found in {args.counties_shp}")
    cook = cook.to_crs(3857)

    # Load HMS polygons day by day
    rows = []
    for d in daterange(start, end):
        y, m, dd = d.strftime("%Y"), d.strftime("%m"), d.strftime("%d")
        shp = pathlib.Path(args.hms_dir)/y/m/f"hms_smoke{y}{m}{dd}.shp"
        if not shp.exists():
            # no file that day -> zero shares
            rows.append({"fips":fips,"date":d,"share_light":0.0,"share_moderate":0.0,"share_heavy":0.0})
            continue
        g = gpd.read_file(shp)[["Density","geometry"]]
        if g.empty:
            rows.append({"fips":fips,"date":d,"share_light":0.0,"share_moderate":0.0,"share_heavy":0.0})
            continue
        g = g.to_crs(3857)
        g["date"] = pd.to_datetime(d.date())
        inter = gpd.overlay(cook, g, how="intersection")
        if inter.empty:
            rows.append({"fips":fips,"date":d,"share_light":0.0,"share_moderate":0.0,"share_heavy":0.0})
            continue
        inter["area"] = inter.geometry.area
        tot = inter.groupby("date", as_index=False)["area"].sum().rename(columns={"area":"area_tot"})
        tmp = inter.merge(tot, on="date", how="left")
        tmp["share"] = (tmp["area"]/tmp["area_tot"]).fillna(0)
        tab = (tmp.pivot_table(index="date", columns="Density", values="share", aggfunc="sum")
                 .fillna(0.0).reset_index())
        tab.columns = ["date"] + [f"share_{c.lower()}" for c in tab.columns[1:]]
        for c in ["share_light","share_moderate","share_heavy"]:
            if c not in tab: tab[c]=0.0
        tab["fips"] = fips
        rows.append(tab[["fips","date","share_light","share_moderate","share_heavy"]].iloc[0].to_dict())

    out = pd.DataFrame(rows).sort_values("date")
    pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(args.out, index=False)
    print(f"Wrote {args.out} with {len(out)} rows")

if __name__ == "__main__":
    main()
