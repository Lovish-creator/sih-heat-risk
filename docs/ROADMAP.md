# Roadmap — ThermoShield India (SIH26083)

**STATUS: STRATEGIC ROADMAP (TIER 1 BASELINE → TIER 2 PILOT → TIER 3 PRODUCTION)**

---

## 1. Development Strategy Overview

The ThermoShield India platform follows a deliberate, disciplined three-tier development strategy:

```
┌────────────────────────────────────────┐
│ TIER 1: Current SIH Working Prototype │ ◄── (Delivered & Verified Scope)
└───────────────────┬────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────┐
│ TIER 2: Data-Connected Pilot Expansion │ ◄── (Future Institutional Integration)
└───────────────────┬────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────┐
│ TIER 3: Long-Term Production System    │ ◄── (National Operational Infrastructure)
└────────────────────────────────────────┘
```

The existence of interfaces, database schemas, configuration files, ML scaffolding, or adapter stubs for future functionality does **NOT** imply that those capabilities are currently implemented.

---

## 2. 3-Tier Capability Comparison Matrix

| Capability | Tier 1: Current Prototype | Tier 2: Pilot | Tier 3: Production |
|---|---|---|---|
| **Weather data** | Public weather and forecast APIs (Open-Meteo, NASA POWER) | Verified operational providers (IMD AWS feeds, NCMRWF connector) | Official multi-source integration (NCUM 4km, GFS, INSAT-3D, AWS networks) |
| **Thermal indices** | UTCI (COST 730 polynomial), WBGT (Stull/Liljegren), NOAA Heat Index | Calibration and validation against ground station networks | Continuous scientific validation & urban microclimate physics coupling |
| **Vulnerability** | Available demographic indicators (Census 2011 PCA baseline) | Verified ward-level datasets from State Municipal Directorates | Dynamic population, real-time mobility, and socio-economic exposure layers |
| **Mortality modelling** | Not implemented (Relative Heat-Health Risk Score 0–100 only) | Historical validation and calibration against municipal health records | Validated mortality/hospitalization models (DLNM exposure-response curves) |
| **Machine learning** | Future extension only (scaffolding with truthfulness guard) | Genuine labelled-data experimentation (GBDT bias correction) | Operational predictive modelling with continuous evaluation and drift monitoring |
| **GIS** | Interactive prototype map (26 DataMeet cities + Stewart-Oke LCZs) | Verified spatial datasets (Survey of India / State GIS portals) | National-scale GIS infrastructure with sub-kilometer satellite LST downscaling |
| **Advisories** | Rule-based prototype advisories (NCDC NAP-HRI 2024 / NDMA) | Tested authority workflows with local municipal disaster cells | Automated multi-channel alerts (NDMA SACHET, SMS, WhatsApp, TV/Radio CAP) |
| **Health integration** | Not connected (transparent spatial prioritization) | Pilot partnerships with selected District Civil Hospitals / IDSP units | Operational surveillance integration (IHIP syndromic feeds, CRS mortality) |
| **Database** | Prototype/local persistence where used (SQLite local cache) | PostgreSQL/PostGIS pilot with spatial indexing | Scalable managed infrastructure with multi-region high availability |
| **Deployment** | Existing hosted demonstration (Vercel serverless / Local FastAPI) | Controlled pilot deployment in 1–2 target Municipal Corporations | Government-grade production deployment on MeghRaj / NIC National Cloud |
| **Validation** | Formula and software tests (51 passing unit & integration tests) | Historical backtesting against past extreme heatwave events | Independent scientific validation by national meteorological & health bodies |

---

## 3. Tier 2 — Data-Connected Pilot / Engineering Expansion

**STATUS: FUTURE DEVELOPMENT**

> *"Tier 2 would convert the prototype into a data-connected pilot through verified datasets, operational ingestion, historical validation, and controlled institutional integration."*

Tier 2 represents the next phase of development following the successful Tier-1 prototype. Its primary objectives are improving data quality, spatial resolution, operational reliability, empirical calibration, and stakeholder usability.

### Planned Tier-2 Capabilities (Future Development)

1. **Verified Administrative Boundaries:** Ingest official municipal ward delimitation GeoJSON/Shapefiles verified by State Election Commissions and Urban Development Departments.
2. **Complete Ward-Level Demographics:** Integrate contemporary municipal survey data and updated Census projections.
3. **PostgreSQL / PostGIS Operational Storage:** Migrate from local prototype persistence to enterprise spatial database storage with spatial indexing (`ST_Contains`, `ST_Intersects`).
4. **Scheduled Ingestion Pipelines:** Deploy Celery / Airflow orchestrators for automated periodic ingestion of NWP model cycles (00, 06, 12, 18 UTC).
5. **Data Validation & Quality Monitoring:** Implement automated anomaly detection, physical range clamping, and sensor drift flagging.
6. **Historical Weather Archives:** Build high-resolution historical weather time-series for retrospective event analysis.
7. **Higher-Resolution Forecast Products:** Integrate 4km NCUM regional deterministic and ensemble forecasts.
8. **Official Provider Integrations:** Connect live IMD and NCMRWF institutional data feeds where data access agreements are granted.
9. **Improved Spatial Downscaling:** Implement high-resolution satellite Land Surface Temperature (LST) blending using Landsat/Sentinel-3 thermal infrared channels.
10. **Legitimate Health Outcome Partnerships:** Establish institutional data sharing with selected municipal health departments for aggregated heat-related illness records.
11. **Epidemiological Calibration:** Fit empirical Distributed Lag Non-linear Models (DLNM) to calibrate relative risk weights against verified local health outcomes.
12. **Historical Backtesting:** Retrospectively backtest the early warning model against major historical heatwaves (e.g., May 2010 Ahmedabad, May 2015 Odisha/Andhra, May 2024 North India).
13. **Uncertainty Estimation:** Quantify and display ensemble spread and forecast confidence intervals.
14. **Versioned Model Management:** Implement formal model registry with parameter versioning, lineage tracking, and rollback capabilities.
15. **Authority-Focused Dashboards:** Provide specialized role-based views for Municipal Commissioners, Chief Medical Officers, and Emergency Operations Centers.
16. **Operational Alert Workflows:** Enable draft-review-approve workflows for municipal disaster coordinators before dispatching public advisories.
17. **Telecom Gateway Integration:** Connect approved government SMS / WhatsApp gateway APIs for broadcast dissemination.
18. **Municipal Pilot Deployment:** Deploy and evaluate the system with 1 or 2 pilot municipal corporations (e.g., Abohar Municipal Corporation, Ahmedabad Municipal Corporation).
19. **Data Freshness Monitoring:** Implement live telemetry freshness heartbeats, alert notifications on upstream latency, and automated fallback switching.
20. **Security, Backup & Disaster Recovery:** Deploy automated database backups, role-based access control (RBAC), audit logs, and encryption at rest.

---

## 4. Tier 3 — Long-Term Production-Scale System

**STATUS: FUTURE VISION**

> *"Tier 3 is the long-term production vision requiring institutional partnerships, validated health data, operational infrastructure, scientific calibration, governance, and government deployment approvals."*

Tier 3 represents the full-scale, nationwide operational vision for India's heatwave early warning infrastructure. It must never be presented as current functionality.

### Planned Tier-3 Capabilities (Future Vision)

1. **National-Scale Multi-State Deployment:** Operational coverage across all 28 states, 8 Union Territories, and 4,000+ urban local bodies (ULBs).
2. **Official NCMRWF & IMD Core Integration:** Direct high-throughput coupling to NCUM 4km/12km numerical weather models, Doppler Weather Radar networks, and national Automatic Weather Station (AWS) grids.
3. **Automated Multi-Source Ingestion:** Resilient, multi-redundant ingestion pipeline processing satellite, radar, ground stations, and numerical forecasts simultaneously.
4. **High-Resolution Urban Numerical Modeling:** Micro-scale urban canopy and heat-island modeling at 100m–500m resolution.
5. **Satellite Land-Surface Thermal Coupling:** Real-time integration of ISRO INSAT-3D/3DR, NASA MODIS, and ESA Sentinel-3 thermal infrared observations.
6. **Dynamic Urban Heat Island (UHI) Modeling:** Physics-based simulation of thermal retention across varying building geometries and asphalt fractions.
7. **High-Resolution Built-Environment & Land-Cover Mapping:** Integration of National Remote Sensing Centre (NRSC) high-resolution land-use/land-cover datasets.
8. **Verified National Health-Surveillance Integration:** Direct integration with Ministry of Health and Family Welfare (MoHFW) Integrated Health Information Platform (IHIP) and Civil Registration System (CRS).
9. **Epidemiologically Validated Mortality Models:** City-specific Minimum Mortality Temperature (MMT) thresholds and non-linear exposure-lag-response functions.
10. **Hospitalization Surge Prediction:** Machine-learning models predicting daily heatstroke emergency room visits and hospital bed demand.
11. **Calibrated Machine-Learning Predictive Models:** Gradient-boosted decision trees and neural networks trained on multi-year verified health and meteorological time-series.
12. **Continuous Model Evaluation & Governance:** Automated tracking of model performance, skill scores, and calibration curves across seasons.
13. **Model Drift & Climate Stationarity Monitoring:** Automated detection of shifting baseline temperatures and changing population vulnerability profiles.
14. **Secure Government API Infrastructure:** API gateway adhering to National Data Sharing and Accessibility Policy (NDSAP) standards with API key management and rate limiting.
15. **Automated Municipal Emergency Alert Dispatch:** Integration with National Disaster Management Authority (NDMA) SACHET Common Alerting Protocol platform.
16. **Multi-Channel Public Communications:** Automated dissemination via Cell Broadcast Emergency Alerts, SMS, WhatsApp, television, community radio, and digital signage.
17. **Multi-Language Advisory Engine:** Natural language generation of culturally contextualized advisories across all 22 official Indian languages.
18. **Fine-Grained Role-Based Access Control:** Tiered permissions for central ministries, state disaster management authorities (SDMAs), district magistrates, and municipal field officers.
19. **Immutable Audit Logging:** Cryptographic audit trails for all issued advisories, alert level escalations, and operator actions.
20. **Disaster Management Interoperability:** Native integration with NDMA National Disaster Emergency Management (NDEM) and State EOC platforms.
21. **National Cloud Infrastructure:** Deployment on MeghRaj (Government of India Cloud) / National Informatics Centre (NIC) high-availability infrastructure.
22. **Data Governance & Statutory Privacy Compliance:** Strict adherence to the Digital Personal Data Protection Act (DPDPA 2023) ensuring health data is completely de-identified and aggregated.
23. **Independent Scientific Validation:** Formal peer-reviewed evaluation by atmospheric scientists, biometeorologists, and public health epidemiologists.
24. **Statutory Government Approvals:** Formal operational commissioning and accreditation by relevant nodal ministries.

---

## 5. Transition Plan: Sequential Path from Tier 1 to Tier 3

The evolution from prototype to production must be methodical, evidence-based, and sequential:

```
Step 1: Freeze Tier 1
  └── Confirm working features, freeze formulas, record data sources and limitations.
      │
Step 2: Verify Data Availability
  └── Identify official data requirements, verify boundary availability and health access.
      │
Step 3: Build the Data Foundation
  └── Deploy operational PostgreSQL/PostGIS, ingestion pipelines, and freshness checks.
      │
Step 4: Improve Scientific Validation
  └── Backtest against past heatwaves, calibrate weights using evidence, quantify uncertainty.
      │
Step 5: Build the Pilot
  └── Deploy in 1–2 target municipal corporations, test with local disaster authorities.
      │
Step 6: Prepare for Tier 3
  └── Expand geography, connect institutional streams, obtain government approvals.
```

### Step 1 — Freeze Tier 1 (Current Milestone)
- Confirm and document all working Tier-1 capabilities.
- Freeze the deterministic biometeorological formulas (UTCI, WBGT, Heat Index) for the SIH demonstration.
- Explicitly record all data sources, assumptions, and fallback behaviors.
- Document all limitations honestly; ensure frontend and backend are 100% consistent.
- Tag the Tier-1 repository baseline.

### Step 2 — Verify Data Availability
- Formally identify required official datasets for target pilot jurisdictions.
- Confirm access permissions and institutional API availability (IMD, NCMRWF, State Municipal Directorates).
- Verify vector boundary availability and Census demographic completeness for candidate pilot cities.
- Identify legitimate historical health outcome datasets (de-identified, aggregated) for empirical calibration.
- Formally record data gaps in the data registry.

### Step 3 — Build the Data Foundation
- Introduce operational PostgreSQL/PostGIS storage for observations, forecasts, ward geometries, and risk outputs.
- Build resilient ingestion pipelines with logging, retry logic, and deduplication.
- Implement automated freshness checks and disable uncontrolled fallback behavior in production mode.
- Establish database migration workflows (`Alembic`) and audit schemas.

### Step 4 — Improve Scientific Validation
- Verify thermal index calculations against international reference benchmarks (COST 730 Fortran/C code).
- Obtain historical weather series for known heatwave events.
- Obtain legitimate aggregated health outcome series where permitted by institutional agreements.
- Backtest risk scores and calibrate multi-criteria weights against real impact data.
- Measure and document false positive / false negative rates and uncertainty bounds.

### Step 5 — Build the Pilot
- Select one or two target deployment regions (e.g. Abohar Municipal Corporation, Ahmedabad Municipal Corporation).
- Load verified municipal ward boundaries and local demographic profiles.
- Connect approved institutional data providers.
- Conduct operational field testing with local municipal disaster management cells and Chief Medical Officers.
- Collect structured feedback on advisory clarity, map usability, and alert timeliness.

### Step 6 — Prepare for Tier 3
- Only after successful Tier-2 pilot validation:
  - Expand geographic coverage state-by-state.
  - Connect institutional NCMRWF 4km NWP streams and NDMA SACHET broadcast gateways.
  - Introduce calibrated machine-learning models only if legitimate training data is available.
  - Establish formal statutory governance, privacy compliance (DPDPA 2023), and 24/7 infrastructure monitoring.
