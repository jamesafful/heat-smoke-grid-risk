SHELL := /bin/bash
PY := python

.PHONY: setup test run-sample lint pilot dirs epa_download counties_download hms_download ingest_pm25 smoke_intersect build_panel clean

setup:
	@echo 'No setup needed for stdlib sample.'

test:
	PYTHONPATH=. pytest -q

run-sample:
	$(PY) -m src.hsg.etl.build_panel_stdlib --sample

# ===== User-tweakable defaults =====
COUNTY ?= 17031             # 5-digit county FIPS, zero-padded
YEAR   ?= 2020
MONTH  ?= 09
# Pilot window (override for whole-month runs)
START_DATE ?= $(YEAR)-$(MONTH)-06
END_DATE   ?= $(YEAR)-$(MONTH)-12

# ===== Paths =====
EPA_DIR      := data/raw/epa
HMS_DIR      := data/raw/hms
COUNTIES_DIR := data/raw/counties
EAGLEI_DIR   := data/raw/eaglei
OUT_DIR      := outputs

COUNTIES_SHP := $(COUNTIES_DIR)/cb_2020_us_county_500k.shp

# ===== Pipeline =====
pilot: dirs epa_download counties_download hms_download ingest_pm25 smoke_intersect build_panel
	@echo "✔ Pilot panel: $(OUT_DIR)/panel_$(COUNTY)_$(START_DATE)_$(END_DATE).parquet"

dirs:
	mkdir -p $(EPA_DIR) $(HMS_DIR)/$(YEAR)/$(MONTH) $(COUNTIES_DIR) $(EAGLEI_DIR) $(OUT_DIR)

# EPA pre-generated daily PM2.5 (88101) CSVs by year
epa_download: | dirs
	curl -fL -o "$(EPA_DIR)/daily_88101_$(YEAR).zip" "https://aqs.epa.gov/aqsweb/airdata/daily_88101_$(YEAR).zip"
	unzip -o "$(EPA_DIR)/daily_88101_$(YEAR).zip" -d "$(EPA_DIR)"

# National counties (cartographic boundaries, 1:500k)
counties_download: | dirs
	curl -fL -o "$(COUNTIES_DIR)/cb_2020_us_county_500k.zip" "https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_county_500k.zip"
	unzip -o "$(COUNTIES_DIR)/cb_2020_us_county_500k.zip" -d "$(COUNTIES_DIR)"

# HMS daily shapefiles for the requested window (handled by a tiny Python helper)
hms_download: | dirs
	$(PY) scripts/fetch_hms.py --start $(START_DATE) --end $(END_DATE) --hms-dir $(HMS_DIR)

# Build PM2.5 county-day mean for the window
ingest_pm25:
	$(PY) scripts/ingest_pm25.py \
	  --county $(COUNTY) \
	  --start $(START_DATE) \
	  --end $(END_DATE) \
	  --epa-dir $(EPA_DIR) \
	  --out "$(OUT_DIR)/pm25_$(COUNTY)_$(START_DATE)_$(END_DATE).parquet"

# Intersect HMS polygons with county to get area shares by density
smoke_intersect:
	$(PY) scripts/smoke_intersect.py \
	  --county $(COUNTY) \
	  --start $(START_DATE) \
	  --end $(END_DATE) \
	  --hms-dir $(HMS_DIR) \
	  --counties-shp "$(COUNTIES_SHP)" \
	  --out "$(OUT_DIR)/smoke_$(COUNTY)_$(START_DATE)_$(END_DATE).parquet"

# Build the panel; if an EAGLE-I CSV for YEAR exists, it will be filtered & aggregated
build_panel:
	$(PY) scripts/build_panel.py \
	  --county $(COUNTY) \
	  --start $(START_DATE) \
	  --end $(END_DATE) \
	  --pm "$(OUT_DIR)/pm25_$(COUNTY)_$(START_DATE)_$(END_DATE).parquet" \
	  --smoke "$(OUT_DIR)/smoke_$(COUNTY)_$(START_DATE)_$(END_DATE).parquet" \
	  --eaglei-csv "$(EAGLEI_DIR)/eaglei_outages_$(YEAR).csv" \
	  --out "$(OUT_DIR)/panel_$(COUNTY)_$(START_DATE)_$(END_DATE).parquet"

clean:
	rm -f $(OUT_DIR)/*.parquet $(OUT_DIR)/*.csv
