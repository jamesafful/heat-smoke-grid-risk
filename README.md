# Heat, Smoke, and Grid Reliability (HSGR)

A research-grade, **data-only** pipeline and analysis skeleton to study associations between **heat waves**, **wildfire smoke**, and **power outages** in the U.S.

- ✅ **Works out-of-the-box** with small **sample datasets** (no internet required) to verify the pipeline.
- 🌐 **Real data fetchers included** (disabled by default). On Codespaces or any internet-enabled environment, flip env flags to fetch public data.
- 🧪 **Unit tests** verify schemas & end-to-end panel build on the sample.
- 📦 Ready for **GitHub Codespaces** or local dev: `make setup && make run-sample`.

> **Scope reality:** This repo ships with *tiny* sample CSVs that mimic the expected schemas (EPA PM2.5 daily, NOAA HMS smoke attributes, EAGLE-I outages). The full public sources are large (ZIPs/shapefiles/GB-scale CSVs). Use the provided fetchers to acquire real data when online.

## Quickstart

```bash
# create & activate virtualenv
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

# run tests & sample pipeline
make test
make run-sample
```

Artifacts are written to `outputs/`, including a sample merged panel and a demo figure.

## Data Sources (for real fetchers)

- **EPA AirData (AQS) PM2.5 daily** pre-generated files (parameter 88101).  
- **NOAA HMS Smoke polygons** (daily shapefile/KML archives).  
- **EAGLE-I historic county outages** (15-minute aggregated CSVs; 2014–2022).  
- **NOAA GHCN/nClimGrid** (for heat-wave indicators; not needed for the sample run).

See `src/hsg/etl/*.py` for URLs, caveats, and instructions. Real downloads are **disabled** by default; enable with `HSGR_ONLINE=1`.

## Commands

```bash
make setup        # lint hooks, etc.
make test         # run pytest
make run-sample   # build panel from sample CSVs and render a demo plot
```

## Structure

```
src/hsg/
  etl/              # fetchers and cleaners
  models/           # simple statistical models (event probability)
  viz/              # plotting utilities
data/sample/        # tiny CSV samples to verify the pipeline
tests/              # pytest unit tests
outputs/            # generated artifacts
```

## License

MIT
