# System Boundaries & Scientific Limitations — ThermoShield India (SIH26083)

In accordance with scientific integrity and transparent engineering principles, this document provides an honest, comprehensive evaluation of the system's operational scope, data resolution limits, and scientific boundaries.

---

## 1. Meteorological Spatial Downscaling vs. Sensor Reality

### The Physical Reality
* True microclimate variation at $\le 200\text{m}$ resolution (e.g. narrow street canyons, localized tree canopy shading, vehicular heat exhaust) cannot be observed by physical AWS stations alone, because no municipal corporation in India operates automated weather stations at $200\text{m}$ grid intervals.
* Regional Numerical Weather Prediction (NWP) models (such as NCMRWF NCUM and IMD GFS) provide operational forcing at $4\text{km}$ to $12\text{km}$ horizontal resolution.

### ThermoShield's Downscaling Approach & Boundary
* ThermoShield computes **Local Climate Zone (LCZ)** biophysical offsets based on Stewart & Oke (2012) classifications, impervious surface fractions, and surface albedo.
* **Limitation:** While these microclimate adjustments account for urban morphology and building density differentials, they represent **parameterized microclimate estimates**, not direct physical sensor measurements. Real-time IoT sensor networks (such as citizen micro-stations or municipal LoRaWAN sensors) can be linked as future data adapters.

---

## 2. Demographic Baseline: Census 2011 vs. Present Dynamics

### The Data Landscape
* The latest official statutory census released by the Office of the Registrar General and Census Commissioner of India (RGI) is **Census 2011 Primary Census Abstract (PCA)**.
* Ward-level elderly counts ($60+$), child populations ($0-5$), and main/marginal informal labor breakdowns are anchored to this decennial statutory baseline.

### System Handling & Boundaries
* Where recent municipal population projections are available, density adjustments are applied.
* **Limitation:** Intra-city migrant worker movement, post-2020 urban expansion, and local construction worker concentrations may differ from decennial enumeration. The vulnerability engine is structured with standardized ingestion hooks for immediate integration of future Census 2026 releases or state-level NFHS-5 surveys.

---

## 3. Ward Geometry Provenance: Surveyed vs. Density-Proportional Delimitations

### The Data Landscape
* Official surveyed GIS shapefiles (sub-meter cadastral polygons) are publicly released for certain metropolitan corporations (e.g., Delhi MCD, Ahmedabad AMC, Mumbai BMC), but are restricted or published solely as text gazettes for smaller statutory towns (e.g., Abohar Municipal Corporation 50-ward gazette).

### Provenance Guardrail
* ThermoShield **never misrepresents generated geometries as official surveyor shapefiles**.
* Every ward feature in the database and API output includes:
  ```json
  "is_official_geometry": false,
  "is_generated_geometry": true,
  "geometry_source": "census_density_proportional_v1"
  ```
* For towns without open GIS shapefiles, boundaries are computed using density-proportional spatial tessellation ($A_w = \text{Pop}_w / \text{Density}_w$) anchored to official ward centroids and municipal delimitation gazettes.

---

## 4. Upstream Telemetry: Public Open Data vs. Restricted IMD / NCMRWF Feeds

### Current Implementation
* ThermoShield utilizes authenticated, high-reliability open data streams:
  - **Open-Meteo Weather API** (15-min surface telemetry & 7-day multi-horizon forecast)
  - **NASA POWER API** (All-sky solar downward irradiance & climatological flux)
  - **IMD Climatological Gazettes** (Official heatwave threshold criteria: $+4.5^\circ\text{C}, +6.4^\circ\text{C}$)

### Roadmap & Integration Hooks
* Production deployment with the Ministry of Earth Sciences (MoES) will ingest direct NCUM $4\text{km}$ GRIB2 model feeds and IMD AWS high-frequency telemetry via dedicated server-side pipeline adapters (`backend/app/ingestion/`).

---

## 5. Health Data Readiness & Anti-Hallucination Policy

### Absolute Rule: Zero Fabricated Clinical Labels
* ThermoShield explicitly **rejects the generation of fake hospital admissions, heat stroke casualties, or synthetic mortality numbers**.
* Fabricating health outcome data violates medical ethics, epidemiological validity, and legal compliance.

### Relative Risk vs. Clinical Outcome
* The composite Heat-Health Risk Index ($R \in [0, 100]$) is a **relative spatial prioritization metric** combining environmental hazard, demographic sensitivity, and heatwave duration.
* It alerts municipal authorities to *which wards require prioritized intervention*, rather than claiming to predict exact clinical mortality counts.
* Full integration requirements for authentic State IDSP / DISHA feeds via Distributed Lag Non-Linear Models (DLNM) are detailed in [`docs/HEALTH_DATA_READINESS.md`](HEALTH_DATA_READINESS.md).
