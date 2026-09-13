# SIH Judge Demonstration & Evaluation Guide — ThermoShield India (SIH26083)

**STATUS: EVALUATION & DEMO GUIDE (TIER 1)**

---

## 1. Quick Orientation for Evaluators

**ThermoShield India** is a decision-support platform for municipal heatwave preparedness. In 3 minutes, evaluators can inspect the entire 6-stage early warning workflow:

```
Weather Ingestion → Thermal Stress (UTCI/WBGT/HI) → Vulnerability (Census) → Relative Risk (0-100) → GIS Prioritization → Multi-Persona Advisories
```

---

## 2. Step-by-Step 5-Minute Demonstration Flow

### Step 1: Overview Dashboard & Current Risk
1. Open the application in your browser (`http://localhost:8000/` or the hosted demonstration URL).
2. Observe the **Relative Heat-Health Risk Index** ($0–100$), the IMD 4-tier alert badge (Green / Yellow / Orange / Red), and the physical biometeorological readings (Physiological UTCI, Occupational WBGT, NOAA Heat Index, Dry-Bulb Air Temperature).
3. Notice the live supporting telemetry grid (Dew Point, Solar Radiation, UV Index, Relative Humidity, 10m Wind Speed, Surface Pressure).

### Step 2: Jurisdiction Selection across India
1. In the top toolbar, open the **Jurisdiction** dropdown.
2. Select **Delhi (NCT) — 290 Wards** to see large municipal corporation scaling.
3. Select **Abohar (Punjab) — 50 Wards** to inspect official Punjab municipal delimitation.
4. Select **Bengaluru (243 Wards)**, **Chennai (155 Wards)**, or **Kolkata (141 Wards)** to observe regional climatic differences (e.g. humid coastal vs. inland).

### Step 3: Interactive GIS Risk Map & Decision-Support Drawer
1. Click the **🗺️ GIS Risk Map** tab in the top navigation.
2. The interactive Leaflet choropleth map renders ward polygons colored by risk level.
3. **Click on any ward polygon on the map**:
   - The **Decision-Support Side Drawer** slides open.
   - It answers: *"Why is this specific unit at elevated risk?"* (e.g., breakdown of high thermal load, elderly concentration, and outdoor worker density).
   - It provides **Targeted Municipal Actions** for that specific ward.
4. Use the **Horizon buttons (D+0 to D+4)** in the toolbar to observe how spatial risk evolves across the 5-day forecast.

### Step 4: GPS Auto-Detection & Global Coordinates
1. Click **📍 Detect Location** in the top header to analyze your current physical location via GPS.
2. Alternatively, click **🌐 Lat/Lon** and enter custom coordinates (e.g., `Latitude: 26.9124, Longitude: 75.7873` for Jaipur) to verify any point in India.

### Step 5: 5-Day Forecast Analytics & 24-Hour Diurnal Cycle
1. Click the **📈 5-Day Forecast** tab.
2. Review the **5-Day Risk Trajectory** chart and the **Biometeorological Index Divergence** chart (which demonstrates why UTCI and WBGT diverge from simple air temperature under humidity/solar radiation).
3. Review the **24-Hour Diurnal Heat Cycle Table** showing hourly temperature, wet-bulb, solar flux, and risk.
4. Read the **Plain-Language Interpretation Box** explaining the meteorological drivers.

### Step 6: Demographic Vulnerability Matrix
1. Click the **👥 Demographic Vulnerability** tab.
2. View the compiled Census of India 2011 Primary Census Abstract (PCA) indicators (Elderly 60+, Outdoor Laborers, Population Density).
3. Type into the filter bar (e.g. "Ward 1" or "RED") to search specific units.
4. Click **📥 Export Risk Data (.CSV)** to test tabular data export for municipal emergency planners.

### Step 7: Actionable Advisories & CAP v1.2 Emergency Alerts
1. Click the **🚨 Actionable Advisories** tab.
2. Observe tailored, actionable guidance across all 4 personas:
   - **General Public & Citizens** (hydration, cooling centers)
   - **Outdoor Laborers & Employers** (mandatory NIOSH hourly labor/rest cycles)
   - **Municipal Disaster Coordinators** (water tanker routing, cooling space activation)
   - **Health & Emergency Response** (heatstroke triage readiness, IV fluid stockpiling)
3. Click the **🚨 CAP Alert** button in the top header to inspect the generated **ITU/WMO Common Alerting Protocol (CAP v1.2)** XML/JSON payload and localized citizen SMS broadcast text.

### Step 8: Data Provenance & Methodology Audit
1. Click the **📖 Data & Provenance Audit** tab.
2. Review the transparent table documenting the source, status, and limitations for every single component.
3. Review the exact mathematical equations and multi-criteria weighting framework.

---

## 3. Key Evaluator Questions & Answers

| Evaluator Question | Engineering Reality & Code Reference |
|---|---|
| *"Is this predicting deaths or hospital cases?"* | **No.** It computes an interpretable **Relative Heat-Health Risk Score (0–100)** to prioritize municipal intervention. We reject ungrounded mortality predictions without daily hospital registry telemetry (Tier 3). |
| *"Are the biometeorological formulas real?"* | **Yes.** Implemented in pure Python: UTCI 6th-order polynomial (`backend/app/thermal/utci.py`), Stull wet-bulb & Liljegren WBGT (`backend/app/thermal/wbgt.py`), and Rothfusz Heat Index (`backend/app/thermal/heat_index.py`). Verified by 51 unit tests. |
| *"Where does the weather data come from?"* | Live open endpoints: **Open-Meteo API** (surface meteorology & forecasts) and **NASA POWER API** (solar irradiance). Verified live in `backend/app/data_sources/open_meteo.py`. |
| *"How is the ward data structured?"* | Bundled GeoJSON boundaries for 26 municipal corporations (DataMeet / delimitation notifications) and Stewart & Oke (2012) Local Climate Zone spatial engine for other towns. |
