# SIH 2026 PS26083 — Repository Implementation Audit

**Platform:** ThermoShield India — Extreme Heatwave Early Warning and Human Thermal Stress Index  
**Audit Date:** September 2026  
**Status:** Pre-Refactoring Baseline Audit  

---

## 1. Comprehensive System Audit Matrix

| Area | Current Implementation | Problem | Required Change | Priority |
|---|---|---|---|---|
| **1. Centralized Configuration** | Scattered hardcoded strings, relative file path search heuristics, and missing environment variable management. | No clear distinction between Development, Demo, and Production modes; no single source of truth for runtime settings. | Implement ackend/app/core/config.py with pydantic-settings supporting APP_ENV, DATA_MODE, DATABASE_URL, ENABLE_FALLBACK_DATA, and LOG_LEVEL. Update .env.example. | **P0 (Critical)** |
| **2. Database & Persistence** | Ephemeral in-memory dictionary cache (cache.py) with filesystem JSON dumps; no relational database. | Data is lost on process restart; no persistent historical forecasts, no observation verification, no relational queries. | Implement SQLAlchemy 2.0 ORM with Alembic migrations supporting SQLite (local dev/test) and PostgreSQL/PostGIS (production). Add 13 normalized tables. | **P0 (Critical)** |
| **3. Administrative Geometry & Ward Data** | Synthesizes radial polygon grids when GeoJSON files are missing; sometimes conflates generated polygons with official municipal delimitations. | Violates Truthfulness Rule #3: generated geometries must never be labeled as official municipal shapes. | Refactor ward_directory.py to strictly separate Administrative Geometry from demographic attributes and explicitly flag is_official_geometry: False and is_generated_geometry: True. | **P0 (Critical)** |
| **4. Demographic Vulnerability & Fallbacks** | demographic.py loads india_census_districts.json and uses a national default fallback when district is unmatched. | Silent fallback in production mode violates Truthfulness Rule #2. | Refactor demographic engine to record is_fallback, allback_reason, source_year, and data_quality. Throw explicit DATA_UNAVAILABLE errors in production mode. | **P0 (Critical)** |
| **5. Scientific Biometeorological Models** | Implements UTCI (COST 730 6th-order), WBGT (Liljegren/Bernard), Heat Index (Rothfusz), and Psychrometrics in ackend/app/thermal/. | Scientific modules are partially tied to schemas; missing input boundary validation and formal engine version metadata. | Pure functional decoupling of scientific algorithms with strict input validation bounds (Ta, RH, wind, solar) and metadata output (engine_version: 1.2.0-scientific). | **P1 (High)** |
| **6. Composite Heat Risk Engine** | HeatRiskEngine combines Thermal Hazard, Vulnerability, and Duration using weights in 
isk_weights.yaml. | Weights are not dynamically validated to ensure sum equals 1.0; risk score needs crystal-clear relative prioritization disclaimer. | Validate weight summation (sum == 1.0 ± 1e-6); return transparent component sub-scores (	hermal_hazard, ulnerability, persistence); explicitly document relative prioritization. | **P1 (High)** |
| **7. External Data Ingestion** | Direct live API calls to Open-Meteo and NASA POWER on frontend load; stub files for IMD/NCMRWF. | Frontend page loads can experience latency or rate-limiting; IMD/NCMRWF connectivity status is not explicitly standardized. | Create unified provider interfaces (BaseWeatherProvider, etc.), add background ingestion scheduler, implement duplicate observation prevention, and expose explicit status for IMD/NCMRWF adapters. | **P1 (High)** |
| **8. Forecast Persistence & Verification** | Generates 5-day forecast horizon dynamically in memory on each request. | Inability to track forecast drift, compare D+1 vs D+5 forecasts against realized observations, or assess forecast accuracy. | Persist D+1 to D+5 forecasts in database; provide forecast freshness metrics and observation-vs-forecast comparison endpoints. | **P1 (High)** |
| **9. Health Data & Epidemiological Readiness** | No health data schema or historical morbidity/mortality linkage. | Risk of developers attempting to train fake ML models or claiming clinical mortality prediction without genuine health data. | Create formal health data architecture (health_records schema) and create docs/HEALTH_DATA_READINESS.md detailing ethical, epidemiological, and privacy constraints. | **P1 (High)** |
| **10. Machine Learning Architecture** | No structured ML package or extension interface. | Future team members might blindly add black-box ML models on fabricated target labels. | Build modular ML scaffolding (ml/ package with datasets, feature engineering, registry) while keeping the deterministic biometeorological model as the active default. | **P2 (Medium)** |
| **11. API Design & Versioning** | FastAPI routes in endpoints.py are mostly at /api/v1/ but lack unified error handling, data freshness headers, and source metadata. | Inconsistent metadata across endpoints; missing standard freshness and fallback indicators in responses. | Standardize all endpoints under /api/v1/ with Pydantic V2 response models including provenance, reshness_timestamp, model_version, and data_quality. | **P1 (High)** |
| **12. Frontend UI / UX & Observability** | Interactive Leaflet GIS dashboard and Chart.js diurnal curves; clean layout. | UI lacks explicit badges showing whether data is live or fallback, and does not show component breakdowns for individual wards. | Add live data source status pills, last-updated freshness timer, fallback warning banners, and detailed component breakdown modal/panels. | **P1 (High)** |
| **13. Alerting & Notification Interface** | Rule-based advisory texts in dvisory/engine.py. | No programmatic alert dispatching, webhook triggers, or structured alert payloads for municipal emergency centers. | Build ackend/app/alerts/engine.py with structured JSON alert schemas and webhook dispatcher with mock delivery logging. | **P2 (Medium)** |
| **14. Docker & Local Orchestration** | Basic Dockerfile exists; docker-compose.yml was minimal. | Local developers lack a one-command setup for backend, frontend, and PostgreSQL/PostGIS. | Provide multi-stage Dockerfile, complete docker-compose.yml with healthchecks, and one-click local startup scripts (
un_local.bat, 
un_local.ps1). | **P1 (High)** |
| **15. Automated Test Suite** | 41 unit & integration tests passing in pytest. | Missing tests for database models, repositories, fallback policy enforcement, and weight sum validation. | Expand test suite to 50+ tests covering all scientific boundaries, database CRUD, fallback enforcement, and alert generation. | **P1 (High)** |
| **16. System Documentation** | Several markdown files exist in docs/ and root. | Incomplete coverage of data dictionaries, health data readiness, model cards, and final implementation status. | Produce complete set of 12 documentation files covering architecture, data dictionaries, provenance, API contracts, and limitations. | **P1 (High)** |

---

## 2. Refactoring Action Plan

1. **Phase 1:** Centralized Configuration (core/config.py, .env.example).
2. **Phase 2:** Database Foundation (SQLAlchemy 2.0, Alembic, 13 ORM models, repositories, seed scripts).
3. **Phase 3:** Ward & Demographic Data Separation (geometry vs demographics vs weather vs risk).
4. **Phase 4:** Data Ingestion Architecture (providers, background scheduler, duplicate prevention).
5. **Phase 5:** Scientific Engine Refactor (pure biometeorological modules with validation).
6. **Phase 6:** Risk Engine Refactor (versioned weights, sum=1.0 validation, component breakdown).
7. **Phase 7:** Forecast Persistence (D+1 to D+5 DB storage & verification).
8. **Phase 8:** Health Data Readiness (docs/HEALTH_DATA_READINESS.md & health schema).
9. **Phase 9:** Optional ML Extension Scaffolding (ml/ package).
10. **Phase 10:** API Versioning & Endpoints (/api/v1/).
11. **Phase 11:** Frontend Observability & Explanations.
12. **Phase 12:** Alert & Webhook Engine.
13. **Phase 13:** Docker & Local Execution Scripts.
14. **Phase 14:** Comprehensive Automated Testing (50+ tests).
15. **Phase 15:** Complete Documentation Deliverables.
