# Reproducing the Data Paper Assets

## 1) Build pilot panels
```bash
make pilot COUNTY=17031 YEAR=2020 MONTH=09 START_DATE=2020-09-06 END_DATE=2020-09-12
make pilot COUNTY=06037 YEAR=2020 MONTH=09 START_DATE=2020-09-06 END_DATE=2020-09-12
make pilot COUNTY=53033 YEAR=2020 MONTH=09 START_DATE=2020-09-06 END_DATE=2020-09-12
python scripts/concat_panels.py --inputs \
  outputs/panel_17031_2020-09-06_2020-09-12.parquet \
  outputs/panel_06037_2020-09-06_2020-09-12.parquet \
  outputs/panel_53033_2020-09-06_2020-09-12.parquet \
  --out outputs/panel_3counties_2020-09-06_2020-09-12.parquet
