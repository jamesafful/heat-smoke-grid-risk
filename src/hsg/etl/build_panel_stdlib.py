import argparse, csv
from pathlib import Path
from ..data_paths import OUTPUTS, DATA_SAMPLE

def read_csv_dicts(path):
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r)

def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)

def build_sample_panel():
    pm = read_csv_dicts(DATA_SAMPLE / "pm25_cook_2019_2020.csv")
    smoke = read_csv_dicts(DATA_SAMPLE / "hms_smoke_2020-09-09.csv")
    out = read_csv_dicts(DATA_SAMPLE / "outages_2018-09-14_sample.csv")

    # Save small artifacts to outputs
    write_csv(OUTPUTS / "pm25_sample.csv", pm, pm[0].keys())
    write_csv(OUTPUTS / "hms_smoke_sample.csv", smoke, smoke[0].keys())
    write_csv(OUTPUTS / "outages_sample.csv", out, out[0].keys())
    return {"pm25_rows": len(pm), "smoke_rows": len(smoke), "outage_rows": len(out)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()
    if args.sample:
        stats = build_sample_panel()
        print(stats)

if __name__ == "__main__":
    main()
