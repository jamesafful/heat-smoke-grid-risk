# Data Licensing & Attribution

This repository ships code, schemas, and small **derived** pilot panels only.

**Sources used by the pipeline:**
- **EPA AQS AirData (daily_88101 PM2.5)** — U.S. Government public data.
- **NOAA NESDIS HMS Smoke Polygons** — U.S. Government public data (analyst-interpreted visible satellite).
- **EAGLE-I outages** — historical outage observations; redistribution may be restricted by the provider.
  We **do not** include EAGLE-I raw interval data. The repository publishes only **county-day aggregates** derived locally from user-supplied interval CSVs.

**Caveats:**
- HMS smoke indicates *detectable* smoke; it does **not** guarantee surface PM₂.₅ (aloft smoke is common).
- EPA daily_88101 files are pre-aggregated by day; county means in our panels are station-weighted daily means.
