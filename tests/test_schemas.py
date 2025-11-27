import csv
from pathlib import Path

def _read(path):
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f); rows = list(r)
        return rows, r.fieldnames

def test_pm25_columns():
    rows, cols = _read(Path("data/sample/pm25_cook_2019_2020.csv"))
    assert set(["state_code","county_code","site_number","date_local","arithmetic_mean","units_of_measure"]).issubset(cols)

def test_hms_columns():
    rows, cols = _read(Path("data/sample/hms_smoke_2020-09-09.csv"))
    assert set(["date","density","poly_id","area_sqkm","centroid_lon","centroid_lat"]).issubset(cols)

def test_outages_columns():
    rows, cols = _read(Path("data/sample/outages_2018-09-14_sample.csv"))
    assert set(["fips_code","county","state","customers_out","run_start_time"]).issubset(cols)
