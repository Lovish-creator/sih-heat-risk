# REST API Reference — ThermoShield India (SIH26083)

**STATUS: REST API SPECIFICATION (TIER 1)**

Base URL: `http://localhost:8000/api/v1` (or hosted Vercel deployment URL)
Swagger Interactive Docs: `http://localhost:8000/docs`
ReDoc Reference: `http://localhost:8000/redoc`

---

## 1. System Health & Telemetry Observability

### `GET /api/v1/health`
Returns application health status, version, and database connectivity.
- **Response:**
  ```json
  {
    "status": "healthy",
    "app_name": "SIH26083-ThermoShield-India",
    "version": "2.0.0-modular",
    "demo_mode": true,
    "timestamp": "2026-09-13T10:56:36Z",
    "database_status": "ONLINE"
  }
  ```

### `GET /api/v1/health/freshness`
Returns real-time data freshness checks, upstream source latencies, and cache status.

### `GET /api/v1/data-status`
Exposes active city profile, cache entries count, and fallback status.

---

## 2. Locations & Geocoding

### `GET /api/v1/locations`
Returns list of all pre-configured municipal corporations and towns.

### `GET /api/v1/locations/{location_id}`
Returns detailed metadata, coordinates, region type, and ward counts for a specific city.

### `GET /api/v1/geocode/reverse`
Reverse-geocodes geographic coordinates to administrative address hierarchy via OpenStreetMap Nominatim.
- **Query Parameters:**
  - `lat` (float, required): Latitude (-90 to +90)
  - `lon` (float, required): Longitude (-180 to +180)

### `GET /api/v1/geocode/search`
Searches global locations by free-text query.
- **Query Parameters:**
  - `q` (string, required): Place or city name (e.g., "Abohar", "Pune")

### `GET /api/v1/geocode/ip`
Resolves approximate location from client IP address.

---

## 3. Meteorological Observations & Forecasts

### `GET /api/v1/weather/current`
Fetches real-time live surface weather for a city or custom coordinates.
- **Query Parameters:**
  - `city` (string, optional, default: "ahmedabad")
  - `lat` (float, optional)
  - `lon` (float, optional)
- **Response:** Current meteorological observations ($T_a, T_{dp}, RH, WS, P, Solar, UV$).

### `GET /api/v1/weather/forecast`
Fetches 5-day daily forecast series (D+1 to D+5).

### `GET /api/v1/weather/hourly`
Fetches 24-hour diurnal hourly weather series with computed biometeorology.
- **Query Parameters:**
  - `city` (string, optional)
  - `lat` (float, optional)
  - `lon` (float, optional)
  - `hours` (integer, optional, default: 24)

---

## 4. Biometeorological Thermal Stress

### `GET /api/v1/thermal/current`
Calculates real-time UTCI, WBGT, Heat Index, and Composite Thermal Hazard score.
- **Query Parameters:**
  - `city` (string, optional)
  - `lat` (float, optional)
  - `lon` (float, optional)

### `GET /api/v1/thermal/{location_id}`
Returns thermal stress analysis for a configured pilot city.

### `POST /api/v1/thermal/calculate`
Direct programmatic biometeorological calculator accepting raw meteorological parameters.
- **Request Body:**
  ```json
  {
    "temp_c": 42.0,
    "relative_humidity_pct": 45.0,
    "wind_speed_10m_m_s": 2.5,
    "solar_radiation_w_m2": 750.0
  }
  ```
- **Response:** Detailed breakdown of UTCI, WBGT, Heat Index, and Thermal Hazard score.

---

## 5. Relative Risk & GIS Spatial Prioritization

### `GET /api/v1/risk/current`
Calculates Relative Heat-Health Risk Score (0–100) and IMD 4-tier alert level.
- **Query Parameters:**
  - `city` (string, optional)
  - `lat` (float, optional)
  - `lon` (float, optional)
  - `consecutive_heat_days` (integer, optional, default: 1)

### `GET /api/v1/map/risk`
Generates GeoJSON `FeatureCollection` representing municipal wards colored by risk score for interactive choropleth maps.
- **Query Parameters:**
  - `city` (string, optional, default: "abohar")
  - `lat` (float, optional)
  - `lon` (float, optional)
  - `day` (integer, optional, default: 1): Horizon day (1 to 5)
  - `consecutive_heat_days` (integer, optional, default: 1)
- **Response:** Standard GeoJSON FeatureCollection with ward polygon geometries and biometeorological properties.

### `GET /api/v1/wards/summary`
Returns tabular summary of all wards for a city sorted by relative risk score.

---

## 6. Public Health Advisories & Emergency Alerts

### `GET /api/v1/advisory`
Generates action-oriented advisory protocols tailored for 4 personas.
- **Query Parameters:**
  - `city` (string, optional)
  - `lat` (float, optional)
  - `lon` (float, optional)
- **Response:**
  - `alert_level`: GREEN | YELLOW | ORANGE | RED
  - `personas`: `general_public`, `outdoor_workers`, `authorities`, `health_emergency`

### `GET /api/v1/alerts/cap`
Generates ITU/WMO Common Alerting Protocol (CAP v1.2) XML/JSON payload and citizen SMS broadcast text.

### `POST /api/v1/alerts/test`
Simulates emergency alert dispatch and validates webhook connectivity.

---

## 7. Data Provenance & Methodology References

### `GET /api/v1/provenance`
Returns metadata registry for all active and reference upstream data sources.

### `GET /api/v1/references/calculations`
Returns detailed mathematical formulation documentation in JSON format.

### `GET /api/v1/references/downscaling`
Returns Local Climate Zone (LCZ) downscaling architecture specification.
