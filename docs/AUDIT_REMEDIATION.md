# Audit Remediation & Integrity Log — Taapamigo (SIH 2026 PS26083)

This document tracks the remediation pass conducted to ensure complete scientific integrity, factual consistency, and defensible methodology for **Taapamigo: Extreme Heat Early Warning & Human Thermal Stress Decision-Support System** (Smart India Hackathon 2026, Problem Statement PS26083).

---

## 1. Reconciliation with Submitted Presentation

The official SIH 2026 presentation slide deck for this project is frozen and cannot be edited. This section provides an explicit technical reconciliation between the slide deck claims and the repository implementation:

1. **Composite Risk Formulation (Slide 3 vs. Slide 4):**
   - **Implemented Formula:** The codebase (`backend/app/risk/engine.py`, `config/risk_weights.yaml`, and `docs/MODEL_SPEC.md`) implements an **additive multi-criteria linear model**:
     $$\text{Composite Risk} = 0.55 \cdot \text{HazardScore} + 0.30 \cdot \text{VulnerabilityScore} + 0.15 \cdot \text{DurationScore}$$
     Range: $[0, 100]$.
   - **Slide 3 Alignment:** Slide 3 explicitly displays this additive model ($0.55\text{ Hazard} + 0.30\text{ Vulnerability} + 0.15\text{ Duration}$).
   - **Slide 4 Reconciled:** Slide 4 displays the shorthand phrase $\text{Risk} = \text{Hazard} \times \text{Vulnerability} \times \text{Duration}$. This is an established disaster-management conceptual framework shorthand (UNDRR paradigm) representing that risk arises from the interaction of hazard, vulnerability, and duration. It is **not** the mathematical calculation formula used in the software engine.

2. **Automated Test Suite Count:**
   - The submitted slides cite "51 automated tests".
   - The repository baseline passed 52 automated tests. During this remediation pass, additional integration tests for data provenance, document consistency, pluggable alerting, and backtesting are being added, raising the verified count. The live test count is dynamically reported by CI (`.github/workflows/ci.yml`).

3. **Spatial Resolution of Hazard (Macro-Hazard vs. Micro-Vulnerability):**
   - The presentation discusses ward-level early warning and risk differentiation.
   - In the implementation, atmospheric telemetry (air temperature, radiation, wind, humidity, and resulting UTCI/WBGT/Heat Index) is computed from city-scale meteorological stations/forecasts (`"hazard_resolution": "city_scale_uniform"`).
   - Spatial risk variation across municipal wards is driven by **hyperlocal demographic vulnerability** (Census 2011 indicators: elderly population density, outdoor labor share, informal settlements) and **Local Climate Zone (LCZ)** microclimate classification.

4. **Census of India 2011 Data Granularity & Demographics:**
   - The presentation cites Census 2011 PCA demographic inputs.
   - In reality, the Census of India Primary Census Abstract (PCA) provides total population, household size, SC/ST status, and broad economic worker categories (Cultivators, Agricultural Labourers, Household Industry, Other Workers).
   - **The PCA does NOT contain age 60+ population data**; age-wise returns are published separately in Census C-Series tables (C-13 and C-14).
   - Furthermore, construction and informal urban laborers cannot be isolated in the PCA (they fall under "Other Workers").
   - Where exact ward/district records were not extracted directly from raw C-Series tables, the counts are explicitly flagged as `"data_quality": "estimated"` or `"is_illustrative": true`.

---

## 2. Master Remediation Traceability Table

| Finding / Issue | Remediation Action Taken | Files Touched | Verification | Status |
| :--- | :--- | :--- | :--- | :--- |
| **P1-01: Derived Census counts labelled as raw PCA** | Added `scripts/audit_data_provenance.py` to flag derived percentages. Explicitly marked `data_quality: estimated` and updated `census_source`. | `data/sample/india_census_districts.json`, `scripts/build_pan_india_census_wards.py`, `backend/app/vulnerability/demographic.py` | `pytest tests/test_data_provenance.py` (Passed) | Fixed |
| **P1-02: PCA age data & worker proxy limitations** | Authored `data/README_DATA_ACQUISITION.md` documenting PCA vs C-13/C-14 tables; defined outdoor worker proxy in `docs/METHODOLOGY.md`. | `data/README_DATA_ACQUISITION.md`, `docs/METHODOLOGY.md` | Manual inspection against Census definitions | Fixed |
| **P1-03: Ahmedabad illustrative ward delimitation** | Compared with DataMeet point offices; labeled Ahmedabad wards as illustrative prototype delimitation (`is_illustrative: true`). | `data/sample/ahmedabad_census_wards.json`, `data/sample/ahmedabad_wards.geojson` | Pytest & UI verification | Fixed |
| **P1-04: City coverage transparency** | Created `scripts/generate_coverage_report.py` and `docs/COVERAGE.md` detailing exact ward counts, polygon sources, and quality levels for all cities. | `scripts/generate_coverage_report.py`, `docs/COVERAGE.md`, `README.md` | Python execution & table generation | Fixed |
| **P2-01: City-scale hazard transparency** | Added `hazard_resolution` field (`city_scale_uniform` / `modelled_lcz_prototype`); externalized LCZ prototype multipliers to YAML with citations. | `backend/app/gis/engine.py`, `backend/app/gis/ward_directory.py`, `config/lcz_prototype_multipliers.yaml`, `docs/METHODOLOGY.md` | API inspection & Pytest (`test_gis.py`) | Fixed |
| **P3-01: Model specification divergence** | Created `docs/MODEL_SPEC.md` as single source of truth; unified constants and version string; harmonized README and docs. | `docs/MODEL_SPEC.md`, `backend/app/core/constants.py`, `tests/test_docs_consistency.py`, `README.md` | `pytest tests/test_docs_consistency.py` | Planned (Phase 3) |
| **P4-01: Mock alert transparency & IMD alignment** | Renamed mock status to `SIMULATED_NOT_SENT`; added `imd_criteria` & `alert_basis`; implemented pluggable `Notifier` interface; verified CAP v1.2. | `backend/app/alerts/engine.py`, `backend/app/alerts/notifiers.py`, `backend/app/api/endpoints.py`, `tests/test_alerts.py` | `pytest tests/test_alerts.py` | Planned (Phase 4) |
| **P5-01: Empirical back-testing validation** | Created `validation/backtest.py` on historical heatwaves (Ahmedabad 2010, Delhi 2024); added `docs/VALIDATION.md` with explicit event-detection disclaimer. | `validation/backtest.py`, `docs/VALIDATION.md`, `tests/test_backtest.py` | Offline pytest & CSV report | Planned (Phase 5) |
| **P6-01: Frontend triplication & repo hygiene** | Consolidated static assets to `public/`; added Vercel rewrite; fixed mojibake; unified UTCI operational bounds; added CI workflow. | `vercel.json`, `backend/app/main.py`, `.github/workflows/ci.yml`, `tests/test_mojibake.py`, `README.md` | `pytest -q`, local runner, Vercel build | Planned (Phase 6) |

---

## 3. Phase 1 Execution Summary (Data Integrity & Provenance)

- **Audit Script & Verification:** Created `scripts/audit_data_provenance.py` and `tests/test_data_provenance.py`. Confirmed that in `data/sample/india_census_districts.json`, 44 of 46 elderly counts and 45 of 46 outdoor worker counts were computed from round percentage multipliers.
- **Truthful Provenance Labels:** Added `"data_quality": "estimated"` and transparent `"method"` strings to all 46 district records in `data/sample/india_census_districts.json` and in `scripts/build_pan_india_census_wards.py`.
- **Census 2011 Table Realities Documented:** Authored `data/README_DATA_ACQUISITION.md` documenting that the Primary Census Abstract (PCA) does not contain age 60+ data (which resides in C-Series tables C-13/C-14), and that PCA worker categories cannot isolate urban informal/construction laborers.
- **Outdoor Worker Definition:** Updated `docs/METHODOLOGY.md` Section 2.5 defining the outdoor worker metric as an operational proxy with documented limitations.
- **Ahmedabad Delimitation Truth:** Verified that upstream DataMeet `Ahmedabad/Ward_office.geojson` provides point coordinates of ward administrative offices rather than boundary polygons. Marked `data/sample/ahmedabad_census_wards.json` and `data/sample/ahmedabad_wards.geojson` as illustrative prototype delimitation (`"is_illustrative": true`, `"data_quality": "illustrative_prototype"`).
- **Automated Coverage Report:** Created `scripts/generate_coverage_report.py` and generated `docs/COVERAGE.md` auditing all 44 supported urban centers.
- **UI & API Exposure:** Updated `backend/app/vulnerability/demographic.py` to propagate `data_quality` in responses, and updated `public/js/app.js` to render an `"Estimated demographic input"` badge in the ward ranking table and hero snapshot.
- **Test Suite Status:** 55 passed in 4.11s.

---

## 4. Phase 2 Execution Summary (Spatial Resolution of Hazard)

- **Documented Hazard Code Paths:** Authored Section 4 of `docs/METHODOLOGY.md` ("Spatial Resolution of Hazard & Microclimate Modeling") explaining that macro-meteorological hazard is ingested at city scale (`"hazard_resolution": "city_scale_uniform"` in `gis/engine.py`), and spatial risk divergence across wards reflects demographic sensitivity and Local Climate Zone (LCZ) morphology.
- **LCZ Configuration Externalized:** Extracted hardcoded multipliers (1.08, 1.30, etc.) from `ward_directory.py` into `config/lcz_prototype_multipliers.yaml`, explicitly tagging them as `"illustrative_prototype_constants"` with literature citation (Stewart & Oke 2012, BAMS).
- **API Tagging:** Added `"hazard_resolution"` (`"city_scale_uniform"` or `"modelled_lcz_prototype"`) and `"hazard_note"` to all ward feature properties, rankings, and metadata blocks in `backend/app/gis/engine.py` and `backend/app/gis/ward_directory.py`.
- **UI Transparency:** Updated the Decision-Support Drawer in `public/js/map.js` to display: *"Spatial Resolution: Hazard is city-scale; ward differences reflect demographic vulnerability & modeled LCZ microclimate exposure."*
- **Test Suite Status:** 56 passed in 6.13s (added `test_lcz_prototype_multipliers_config` and `hazard_resolution` assertions).

