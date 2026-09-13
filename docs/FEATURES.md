# Features — ThermoShield India (SIH26083)

**STATUS: TIER 1 CONFIRMED DEMONSTRABLE FEATURES**

---

## 1. Real-Time Meteorological Ingestion

- **Public Weather Connection:** Ingests live surface temperature, dew point, relative humidity, wind speed, wind direction, atmospheric pressure, cloud cover, and UV index via Open-Meteo public endpoints.
- **Solar Irradiance Ingestion:** Retrieves surface downward shortwave solar radiation ($W/m^2$) and direct normal irradiance from NASA POWER.
- **Any-Location Coordinate Support:** Allows user to analyze any geographic coordinate across India via GPS auto-detection, interactive map clicks, or manual latitude/longitude input.
- **OpenStreetMap Nominatim Geocoding:** Automatically resolves coordinates to human-readable address hierarchies (ward, town, district, state).

---

## 2. Rigorous Biometeorological Physics Engine

- **Universal Thermal Climate Index (UTCI):**
  - Evaluates equivalent temperature based on the 187-node human thermoregulation model.
  - Implements the official COST 730 6th-order polynomial approximation across 10 biometeorological stress categories (from Extreme Cold Stress to Extreme Heat Stress $>+46^\circ\text{C}$).
- **Wet Bulb Globe Temperature (WBGT):**
  - Implements Roland Stull's (2011) psychrometric wet-bulb temperature formulation ($T_w$).
  - Implements Liljegren black globe temperature estimation ($T_g$) accounting for convective and radiative heat exchange.
  - Generates outdoor WBGT ($0.7 T_w + 0.2 T_g + 0.1 T_a$) and indoor/shade WBGT ($0.7 T_w + 0.3 T_a$).
  - Maps to NIOSH (2016) / ISO 7243 occupational risk levels and hourly labor/rest regimen recommendations.
- **NOAA/NWS Heat Index:**
  - Implements the 9-parameter Rothfusz polynomial regression with Steadman low-range boundary.
  - Categorizes into Caution, Extreme Caution, Danger, and Extreme Danger.
- **Normalized Composite Thermal Hazard:**
  - Harmonizes multi-index metrics into a single continuous Thermal Hazard Score on a $[0, 100]$ scale.

---

## 3. Census 2011 Demographic Vulnerability Engine

- **Census PCA Integration:** Pre-compiled baseline tables covering 46 Indian districts derived from Census of India 2011 Primary Census Abstract (PCA).
- **Vulnerability Indicators:**
  - Elderly population proportion (Age 60+).
  - Outdoor agricultural and daily-wage marginal labor exposure.
  - Population density per square kilometer.
- **Normalized Vulnerability Score:** Synthesizes a demographic vulnerability score on a $[0, 100]$ scale.
- **Fallback Proxy Handling:** Unlisted towns utilize a transparent state-level or national baseline proxy clearly labeled as a fallback baseline.

---

## 4. Relative Heat-Health Risk Engine

- **Interpretable Risk Formula:**
  $$\text{Relative Risk} = (0.55 \times \text{Thermal Hazard}) + (0.30 \times \text{Demographic Vulnerability}) + (0.15 \times \text{Heat Duration Factor})$$
- **Heatwave Duration Multiplier:** Evaluates consecutive heat days ($T_{\max} \ge 40^\circ\text{C}$ or departure $\ge +4.5^\circ\text{C}$) scaling hazard from $1.0\times$ up to $1.4\times$.
- **IMD 4-Tier Alert Classification:** Maps continuous risk scores to official Indian meteorological alert levels:
  - **GREEN (Normal):** Risk $< 25$
  - **YELLOW (Watch):** Risk $25 - 49$
  - **ORANGE (Alert):** Risk $50 - 74$
  - **RED (Warning):** Risk $\ge 75$

---

## 5. GIS Municipal Ward Map & Decision-Support Drawer

- **Interactive Leaflet Choropleth Map:** Visualizes municipal ward boundaries colored by their relative heat-health risk score.
- **26 Available Municipal Corporations:** Includes pre-packaged delimitation vector boundaries for major urban centers (Delhi 290 wards, Bengaluru 243 wards, Chennai 155 wards, Kolkata 141 wards, Hyderabad 145 wards, Lucknow 112 wards, Abohar 50 wards, etc.).
- **Stewart & Oke (2012) LCZ Spatial Engine:** For statutory towns without released municipal GIS vector shapefiles, dynamically generates Local Climate Zone spatial units.
- **Decision-Support Side Drawer ("Why is this location high risk?"):** Clicking any ward opens an explanatory panel detailing:
  - Exact thermal index values ($T_a, UTCI, WBGT, HI$).
  - Key demographic drivers (e.g., "High outdoor worker density: 35%").
  - Targeted municipal action recommendations for that specific ward.

---

## 6. Multi-Horizon Forecast Analytics (D+0 to D+4)

- **5-Day Risk Trajectory:** Interactive Chart.js time-series displaying predicted daily relative risk.
- **Biometeorological Comparison Chart:** Compares UTCI vs. WBGT vs. Heat Index vs. Air Temperature across all 5 forecast days.
- **Meteorological Driver Trends:** Displays trends in maximum temperature, relative humidity, and solar radiation.
- **24-Hour Diurnal Heat Cycle Table:** Hourly breakdown of diurnal temperature, moisture, solar flux, and thermal stress.
- **Plain-Language Interpretation Box:** Contextual summary explaining why risk is projected to rise, fall, or persist.

---

## 7. Actionable Public Health & Occupational Advisories

- **4 Structured Target Personas:**
  1. **General Public & Vulnerable Citizens:** Hydration targets, cooling space guidance, medication warnings.
  2. **Outdoor Workers & Employers:** NIOSH work-rest cycles (e.g., 25% work / 75% rest per hour), shift adjustment directives.
  3. **Municipal Disaster Coordinators:** Water tanker routing, emergency cooling center activation, ward prioritization.
  4. **Health & Emergency Response:** Heatstroke triage readiness, IV fluid stockpiling, hospital surge protocols.
- **Common Alerting Protocol (CAP v1.2) Generator:** Generates standardized XML/JSON payloads and SMS broadcast text formatted for NDMA / SDMA emergency systems.

---

## 8. Data Provenance & Methodology Audit Dashboard

- **In-App Transparency Matrix:** Dedicated UI tab explaining data provenance, update frequencies, access methods, and exact formulas for every single component.
- **Direct Interactive Calculator:** Lets users adjust temperature, humidity, wind, and solar radiation to observe instant biometeorological index recalculations.
