# Data Dictionary — heat-smoke-grid-risk (v1.0-data-paper)

Version: **v1.0-data-paper**  
Scope: County–day panel linking wildfire smoke, PM2.5, and power outages  
Primary output example: `outputs/panel_17031_2020-09-06_2020-09-12.parquet` (and `.csv`)

## 1) Dataset-Level Metadata

- **Spatial unit:** U.S. counties (5-digit FIPS)
- **Temporal unit:** Daily (calendar dates, local-day aligned in processing)
- **Sources:**
  - EPA AQS daily PM2.5 (parameter 88101) — `data/raw/epa/daily_88101_YYYY.csv`
  - NOAA HMS smoke polygons — `data/raw/hms/YYYY/MM/hms_smokeYYYYMMDD.*`
  - DOE EAGLE-I outages — `data/raw/eaglei/eaglei_outages_YYYY.csv` (15-min snapshots)
  - U.S. Census 2020 counties (cartographic) — `data/raw/counties/cb_2020_us_county_500k.*`
- **Processing:** `scripts/ingest_pm25.py`, `scripts/smoke_intersect.py`, `scripts/build_panel.py` (orchestrated by `make pilot …`)
- **File formats:** Parquet and CSV
- **License:** MIT (code), recommend CC BY 4.0 (derived data)

---

## 2) Table: County–Day Panel Schema

Output files of the form:  
`outputs/panel_<FIPS>_<START_DATE>_<END_DATE>.parquet` and `.csv`

| Column            | Type              | Units / Values                        | Description                                                                 | Provenance                                                          |
|-------------------|-------------------|----------------------------------------|-----------------------------------------------------------------------------|---------------------------------------------------------------------|
| `fips`            | string (5 chars)  | e.g., `"17031"`                        | County FIPS code (zero-padded).                                             | Derived from Census counties shapefile; carried through all merges. |
| `date`            | date (YYYY-MM-DD) | calendar day                           | Analysis day. For outages, 15-min snapshots are collapsed to this day.      | Constructed in each script; merges by `fips`+`date`.                |
| `pm25_mean`       | float64           | µg/m³                                   | County-day mean PM2.5 from AQS site-level means for parameter 88101.        | `scripts/ingest_pm25.py` from `daily_88101_YYYY.csv`.               |
| `share_light`     | float64           | 0.0–1.0                                 | Fraction of county area classified “Light” smoke by HMS on that day.        | `scripts/smoke_intersect.py` (HMS polygons ∩ county geometry).      |
| `share_moderate`  | float64           | 0.0–1.0                                 | Fraction of county area classified “Moderate” smoke by HMS on that day.     | Same as above.                                                      |
| `share_heavy`     | float64           | 0.0–1.0                                 | Fraction of county area classified “Heavy” smoke by HMS on that day.        | Same as above.                                                      |
| `cust_out_peak`   | int64             | customers                               | Maximum customers reported out within the day (15-min snapshots → daily).   | `scripts/build_panel.py` from EAGLE-I CSV.                          |
| `cust_out_sum`    | int64             | customers                               | Sum of customers out across snapshots within the day (exposure proxy).      | `scripts/build_panel.py`.                                           |
| `total_customers` | int64             | customers                               | Reported total customers served (max over the day).                          | `scripts/build_panel.py`.                                           |
| `event_any`       | int64 (0/1)       | 0 or 1                                  | Indicator: 1 if `cust_out_peak > 0` else 0.                                 | `scripts/build_panel.py`.                                           |

**Notes & conventions**
- Missing HMS coverage on a day → `share_*` default to `0.0` after merge.
- Days with no outage records → `cust_out_peak=0`, `cust_out_sum=0`, `event_any=0`, `total_customers` may be `0` if absent in source.
- PM2.5 uses AQS *local conditions* field `Arithmetic Mean` for parameter **88101** (regulatory FRM/FEM). Other parameters are not included.

---

## 3) Intermediate Products

- **PM2.5:** `outputs/pm25_<FIPS>_<START>_<END>.parquet`  
  Columns: `date`, `pm25_mean`
- **Smoke shares:** `outputs/smoke_<FIPS>_<START>_<END>.parquet`  
  Columns: `fips`, `date`, `share_light`, `share_moderate`, `share_heavy`
- **Outages (daily aggregates):** e.g., `outputs/outages_cook_2020-09-06_12.parquet`  
  Columns: `fips_code` (int), `date`, `cust_out_peak`, `cust_out_sum`, `total_customers`

---

## 4) Quality Checks Performed (Pilot)

- Schema alignment on `fips` + `date` (inner/left merges audited).
- Value ranges: `0.0 ≤ share_* ≤ 1.0` and `share_light + share_moderate + share_heavy ≤ 1.0`.
- PM2.5 present for each day in range where AQS has coverage.
- Outage aggregates computed from within-day snapshots.

---

## 5) Reproducibility

Recreate pilot panel for Cook County, 6–12 Sep 2020:

```bash
make pilot COUNTY=17031 YEAR=2020 MONTH=09 START_DATE=2020-09-06 END_DATE=2020-09-12
