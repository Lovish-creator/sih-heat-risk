# Model Card — ThermoShield India (SIH26083)

Following the AI/ML and Biometeorological Model Reporting Standards (Mitchell et al., 2019).

---

## 1. Model Details

* **Model Name:** ThermoShield India Biometeorological & Heat-Health Risk Engine
* **Version:** `1.2.0-scientific`
* **Model Type:** Deterministic Biometeorological Physics Engine + Multi-Criteria Demographic Vulnerability Assessment + Optional Statistical/ML Microclimate Downscaler
* **Developers:** SIH 2026 Team (PS26083: Extreme Heatwave Early Warning and Human Thermal Stress Index)
* **Target Domain:** Pan-India Urban Wards & Municipal Corporations
* **License:** MIT License

---

## 2. Intended Use

### 2.1 Primary Intended Uses
1. **Micro-Scale Thermal Stress Mapping:** Providing ward-level Universal Thermal Climate Index (UTCI), Wet Bulb Globe Temperature (WBGT), and Heat Index (HI) for Indian cities.
2. **Municipal Resource Prioritization:** Enabling Municipal Corporations and District Disaster Management Authorities (DDMAs) to identify high-risk wards for targeted deployment of water tankers, cooling shelters, and emergency medical personnel.
3. **Public Health Early Warning:** Generating persona-targeted heat advisories for outdoor laborers, senior citizens, and civic administrators.

### 2.2 Out-of-Scope & Prohibited Uses
* **Individual Medical Diagnosis:** The system does not diagnose clinical heat stroke or prescribe individualized clinical treatments.
* **Absolute Mortality Estimation:** The system provides *relative spatial prioritization*, not absolute statistical casualty counts.
* **Aviation or Micro-Navigation Safety:** The meteorological models are parameterized for human bioclimatic exposure, not aeronautical operations.

---

## 3. Factors and Inputs

### 3.1 Atmospheric Telemetry Inputs
* Ambient Air Temperature ($T_a \in [-50^\circ\text{C}, +60^\circ\text{C}]$)
* Relative Humidity ($\text{RH} \in [0\%, 100\%]$)
* Wind Speed at 10m ($v_{10m} \in [0.1\text{ m/s}, 50.0\text{ m/s}]$)
* Mean Radiant Temperature / Solar Irradiance ($T_{mrt} \in [-50^\circ\text{C}, +100^\circ\text{C}]$, $G \ge 0\text{ W/m}^2$)

### 3.2 Demographic & Spatial Inputs
* Census of India 2011 Primary Census Abstract (PCA)
* Population density (persons / $\text{km}^2$)
* Elderly population share (Age $60+\%$)
* Informal outdoor labor share ($\%$)
* Local Climate Zone (LCZ) classification

---

## 4. Evaluation and Validation

### 4.1 Physical Bounds Validation
All mathematical engines enforce strict physical boundary checks. Out-of-range atmospheric inputs raise explicit validation errors (`ValueError`) preventing unphysical calculations:
* $\text{RH} < 0\%$ or $\text{RH} > 100\%$ $\rightarrow$ Blocked.
* $v_{10m} < 0\text{ m/s}$ $\rightarrow$ Blocked.
* $T_a < -50^\circ\text{C}$ or $T_a > 60^\circ\text{C}$ $\rightarrow$ Blocked.

### 4.2 Automated Test Suite
* **Unit & Integration Tests:** 50 automated tests covering all modules (`pytest tests/`).
* **Test Pass Rate:** 100% (50 / 50 passing).
* **Coverage Areas:** Pure biometeorology (UTCI, WBGT, Heat Index), Demographic Vulnerability, Database CRUD, Ingestion Pipelines, CAP Alert generation, and REST API endpoints.

---

## 5. Ethical Considerations & Provenance Guardrails

1. **Anti-Hallucination Policy on Health Data:**
   - No synthetic mortality or morbidity labels are generated or used for ML training.
   - Ground-truth health records must originate from official State IDSP / DISHA portals under ethical review.
2. **Transparent Geometry Tagging:**
   - Every ward boundary is explicitly stamped as surveyed (`is_official_geometry: true`) or density-proportional generated (`is_generated_geometry: true`).
3. **Data Provenance:**
   - All meteorological sources (Open-Meteo, NASA POWER, IMD normals) are cited with full URLs and update timestamps.
