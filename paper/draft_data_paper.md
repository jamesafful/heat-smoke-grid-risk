# Linking Wildfire Smoke, Fine Particulate Matter, and Power Outages:  
## A Reproducible County-Day Dataset for the United States

---

## Abstract
We present an open, reproducible dataset that links daily wildfire smoke extent, fine particulate pollution (PM₂.₅), and electric-grid outages at the U.S. county level.  
The dataset integrates three public sources:  
1. **U.S. EPA Air Quality System (AQS)** daily PM₂.₅ observations (parameter 88101),  
2. **NOAA Hazard Mapping System (HMS)** daily smoke-density shapefiles, and  
3. **DOE EAGLE-I** power-outage reports.  

The workflow harmonizes these inputs into a single county-day panel using open-source tools and a transparent Makefile pipeline.  
A pilot dataset for **Cook County, Illinois (FIPS 17031)** spanning **6–12 September 2020** demonstrates feasibility: outages occurred on the two days with the highest PM₂.₅ and HMS-detected smoke coverage.  
All code and data are openly available to enable replication and scaling to additional counties and years.

---

## Background & Summary
Wildfire smoke affects air quality and can stress electric grids by increasing cooling demand and degrading transmission equipment.  
However, datasets that link smoke exposure, ambient PM₂.₅ concentrations, and power-outage events at consistent spatial and temporal resolution are rare.  

This project constructs such a dataset using only public, machine-readable sources and minimal dependencies.  
The repository (`heat-smoke-grid-risk`) automates data download, cleaning, spatial intersection, and panel construction through a reproducible `make pilot` command.  

The pilot release focuses on **Cook County, IL**, for **6–12 September 2020**—an interval of regional smoke transport from western wildfires—to validate end-to-end processing.  
The same pipeline generalizes to any U.S. county and time window by changing Makefile parameters:  
`COUNTY`, `YEAR`, `MONTH`, `START_DATE`, `END_DATE`.

---

## Methods

### Data Sources
| Source | Description | Native Frequency | Access Path |
|---------|--------------|------------------|--------------|
| **EPA AQS (88101)** | Daily PM₂.₅ measurements from ground monitors | Daily | `data/raw/epa/daily_88101_2020.csv` |
| **NOAA HMS Smoke Polygons** | Daily shapefiles classifying smoke density (*Light*, *Moderate*, *Heavy*) | Daily | `data/raw/hms/{YYYY}/{MM}/hms_smokeYYYYMMDD.shp` |
| **DOE EAGLE-I Outages** | Utility-reported outages with customer counts and timestamps | ≤ Hourly | `data/raw/eaglei/eaglei_outages_2020.csv` |
| **U.S. Census Counties** | 2020 cartographic boundary shapefile (1:500k) | Static | `data/raw/counties/cb_2020_us_county_500k.shp` |

---

### Processing Pipeline
The Makefile orchestrates the following stages:

1. **EPA Download & Ingest (`ingest_pm25.py`)**  
   - Extracts PM₂.₅ (`Arithmetic Mean`) values for the specified county and date range.  
   - Aggregates monitor-level data to a county-day mean (`pm25_mean`).

2. **Smoke Intersection (`smoke_intersect.py`)**  
   - Reads HMS shapefiles for each day, reprojects to match county geometry.  
   - Computes county-level area shares under each density class (`share_light`, `share_moderate`, `share_heavy`).

3. **Outage Aggregation (`build_panel.py`)**  
   - Filters EAGLE-I records for the target county and date window.  
   - Derives daily outage peaks and sums (`cust_out_peak`, `cust_out_sum`, `total_customers`).  
   - Flags outage occurrence (`event_any = 1` if `cust_out_peak > 0`).

4. **Panel Assembly**  
   - Merges PM₂.₅, smoke, and outage data by `fips` and `date`.  
   - Exports `*.parquet` and `*.csv` to `outputs/`.

**Execution example:**
```bash
make pilot COUNTY=17031 YEAR=2020 MONTH=09 START_DATE=2020-09-06 END_DATE=2020-09-12


---


## Data Records

| File | Description | Rows | Columns |
|------|--------------|-------|----------|
| `outputs/pm25_17031_2020-09-06_2020-09-12.parquet` | County-day mean PM₂.₅ | 7 | `date`, `pm25_mean` |
| `outputs/smoke_17031_2020-09-06_2020-09-12.parquet` | HMS smoke shares | 7 | `fips`, `date`, `share_light`, `share_moderate`, `share_heavy` |
| `outputs/outages_cook_2020-09-06_12.parquet` | Daily outage aggregates | 6 | `fips_code`, `date`, `cust_out_peak`, `cust_out_sum`, `total_customers` |
| `outputs/panel_17031_2020-09-06_2020-09-12.parquet` | Merged county-day panel | 7 | All variables combined |

---

## Variables

| Variable | Type | Unit / Definition |
|-----------|------|-------------------|
| `fips` | string | 5-digit county FIPS code |
| `date` | date | Local day (UTC 00:00–24:00) |
| `pm25_mean` | float | Mean PM₂.₅ (µg m⁻³) |
| `share_light`, `share_moderate`, `share_heavy` | float | Fraction of county area under each smoke density |
| `cust_out_peak` | int | Max customers out in day |
| `cust_out_sum` | int | Sum of customers out across records in day |
| `total_customers` | int | Total customers served in county |
| `event_any` | int (0/1) | 1 if any outage recorded that day |

---

## Technical Validation

### Temporal Coverage
- **PM₂.₅:** 2020-01-01 → 2020-12-31  
- **HMS Smoke:** 2020-09-06 → 2020-09-12  
- **EAGLE-I Outages:** 2020-09-06 → 2020-09-11 18:15  

### Schema Consistency
All tables contain matching `fips` and `date` keys.

### Descriptive Statistics (Cook County, 2020-09-06 – 2020-09-12)
- Mean PM₂.₅ = 5.53 µg/m³ (σ = 2.17)  
- `event_any = 1` on 3 of 7 days (43 %)  
- Outages coincide with the two highest PM₂.₅ days and presence of HMS smoke.  

### Correlation Check
`pm25_mean` and `share_light` r ≈ 0.60, confirming smoke–PM association.  
No missing or invalid values were found in the merged pilot panel.

---

## Usage Notes

The pipeline is parameterized for reproducibility across any county and date range:

```bash
make pilot COUNTY=<FIPS> YEAR=<YYYY> MONTH=<MM> START_DATE=<YYYY-MM-DD> END_DATE=<YYYY-MM-DD>


---

## Potential Applications

The dataset and pipeline can be used for a variety of research and applied purposes, including:

- **Assessing compound heat-and-smoke risks** to electric-grid reliability  
- **Studying health and infrastructure impacts** of wildfire smoke exposure  
- **Benchmarking outage prediction models** using environmental covariates  

Outputs are provided in **Parquet format** for efficient analysis in **Python**, **R**, or **DuckDB**.

---

## Code Availability

**Repository:** [https://github.com/jamesafful/heat-smoke-grid-risk](https://github.com/jamesafful/heat-smoke-grid-risk)  
**License:** MIT (software) / CC-BY-4.0 (data)  

**Core dependencies:**  
`Python 3.10+`, `pandas`, `geopandas`, `duckdb`, `pyproj`, `shapely`, `requests`

---

## Acknowledgements

We acknowledge the following U.S. public agencies for making their data openly available:

- **U.S. Environmental Protection Agency (EPA)** — Air Quality System (AQS)  
- **National Oceanic and Atmospheric Administration (NOAA)** — Hazard Mapping System (HMS)  
- **U.S. Department of Energy (DOE)** — EAGLE-I Outage Reports  
- **U.S. Census Bureau** — Cartographic Boundary Files  

Their continued commitment to open data made this reproducible research possible.

---

## References

- U.S. EPA Air Quality System (AQS) Data Mart — <https://www.epa.gov/aqs>  
- NOAA Hazard Mapping System Smoke Product — <https://www.ospo.noaa.gov/Products/land/hms.html>  
- DOE EAGLE-I Outage Reports — <https://www.energy.gov/ceser/eagle-i>  
- U.S. Census Bureau Cartographic Boundary Files (2020) — <https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html>
