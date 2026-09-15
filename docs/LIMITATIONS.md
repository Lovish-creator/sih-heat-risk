# Technical Limitations & Boundaries — Taapamigo (SIH26083)

**STATUS: TRANSPARENT TECHNICAL BOUNDARIES (TIER 1)**

---

## 1. Ethical & Scientific Boundaries

1. **Not a Clinical Mortality or Morbidity Predictor:**
   The Relative Heat-Health Risk Score ($0–100$) represents relative environmental and demographic exposure to prioritize municipal emergency interventions. It does **not** estimate absolute numbers of deaths, heatstroke admissions, or individual medical risk.

2. **No Patient-Level or Hospital Telemetry:**
   The system does not ingest private electronic health records (EHR), emergency department registers, or syndromic surveillance feeds. All demographic inputs are aggregated public statistics.

3. **No Unvalidated Machine Learning Claims:**
   The repository does not train machine-learning models on synthetic data. ML components are structured as future research scaffolding awaiting verified historical health outcome datasets.

---

## 2. Meteorological & Physical Boundaries

1. **Resolution of Meteorological Inputs:**
   Weather inputs are retrieved from Open-Meteo and NASA POWER public endpoints (global numerical model outputs and satellite reanalysis at $4\text{km} - 11\text{km}$ grid resolution). The system does not possess dedicated physical automated weather stations in every municipal ward.

2. **Microclimate Downscaling Approximations:**
   Sub-grid spatial variation across municipal wards is modeled using Stewart & Oke (2012) Local Climate Zone (LCZ) urban density adjustments ($A_w = \text{Pop}_w / \text{Density}_w$). While physically grounded in urban climatology literature, this remains an algorithmic approximation pending high-resolution urban canopy sensors.

3. **Polynomial Operational Ranges:**
   - The UTCI 6th-order polynomial approximation is valid within $-50^\circ\text{C} \le T_a \le +60^\circ\text{C}$ and $v_{10m} \le 30.3\text{ m/s}$.
   - Stull psychrometric wet-bulb formulation is valid within $-20^\circ\text{C} \le T_a \le +50^\circ\text{C}$ and $5\% \le RH \le 99\%$.
   - Input values outside these physical bounds are clamped defensively with warning logs.

---

## 3. Demographic & Geospatial Boundaries

1. **Census of India 2011 Baseline:**
   Demographic vulnerability indicators (Elderly 60+, Outdoor labor fraction, Population density) are compiled from the Census of India 2011 Primary Census Abstract (PCA). While this represents the most comprehensive official public baseline available, contemporary demographic growth and migration patterns over the past decade are not dynamically captured.

2. **Municipal Boundary Availability:**
   Official digital GIS vector boundaries are bundled for 26 Indian municipal corporations where open civic GIS data (DataMeet) or state delimitation notifications exist. For other statutory towns, algorithmic LCZ spatial units demonstrate Pan-India coverage.

3. **Fallback Proxy Notice:**
   For towns without compiled district Census tables, the system uses a transparent state or national baseline proxy clearly labeled as a fallback.

---

## 4. Operational & Institutional Boundaries

1. **Institutional Upstream Connections:**
   Direct binary GRIB/NetCDF feeds from NCMRWF supercomputers and internal IMD push APIs require formal institutional access agreements (modeled as Tier-2 interfaces).

2. **Automated Alert Dissemination:**
   The platform generates standardized Common Alerting Protocol (CAP v1.2) XML/JSON payloads and SMS broadcast text. Direct automated dispatch to telecom cellular towers or NDMA SACHET requires institutional gateway integration in Tier 2.

3. **Production Deployment Requirements:**
   Full operational commissioning requires deployment on dedicated government cloud infrastructure (MeghRaj / NIC), empirical calibration against local hospital records, and statutory nodal ministry approvals.
