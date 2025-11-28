#!/usr/bin/env python
import argparse, pathlib, datetime, subprocess, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True)  # YYYY-MM-DD
    ap.add_argument("--end", required=True)    # YYYY-MM-DD
    ap.add_argument("--hms-dir", default="data/raw/hms")
    args = ap.parse_args()

    try:
        d0 = datetime.date.fromisoformat(args.start)
        d1 = datetime.date.fromisoformat(args.end)
    except Exception as e:
        print("Bad date format, expected YYYY-MM-DD:", e, file=sys.stderr)
        sys.exit(2)

    cur = d0
    while cur <= d1:
        y = cur.strftime("%Y"); m = cur.strftime("%m"); d = cur.strftime("%d")
        url = f"https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/Shapefile/{y}/{m}/hms_smoke{y}{m}{d}.zip"
        dest_dir = pathlib.Path(args.hms_dir)/y/m
        dest_dir.mkdir(parents=True, exist_ok=True)
        zip_path = dest_dir/f"hms_smoke{y}{m}{d}.zip"
        print("Downloading", url, "->", zip_path)
        subprocess.run(["curl","-fL","-o",str(zip_path),url], check=False)
        if zip_path.exists() and zip_path.stat().st_size > 0:
            subprocess.run(["unzip","-o",str(zip_path),"-d",str(dest_dir)], check=False)
        cur += datetime.timedelta(days=1)

if __name__ == "__main__":
    main()
