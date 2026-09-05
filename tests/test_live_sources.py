"""
Unit and Integration Tests for Real Live Open Data APIs (Open-Meteo & OpenStreetMap Nominatim).
"""

import pytest
import sys
import os
from starlette.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.main import app
from backend.app.data_sources.open_meteo import OpenMeteoProvider
from backend.app.data_sources.geocoding import NominatimGeocoder

client = TestClient(app)


def test_open_meteo_provider_live_or_fallback():
    """Verify Open-Meteo live provider returns valid meteorological variables."""
    provider = OpenMeteoProvider()
    
    # Test for Ahmedabad coordinates (23.0225, 72.5714)
    current = provider.get_current_weather(23.0225, 72.5714, "ahmedabad")
    assert "temp_c" in current
    assert "relative_humidity_pct" in current
    assert "wind_speed_10m_m_s" in current
    assert "solar_radiation_w_m2" in current
    assert -10.0 <= current["temp_c"] <= 60.0
    assert 0.0 <= current["relative_humidity_pct"] <= 100.0
    assert current["wind_speed_10m_m_s"] >= 0.5


def test_open_meteo_forecast():
    """Verify multi-day forecast retrieval from Open-Meteo."""
    provider = OpenMeteoProvider()
    forecast = provider.get_forecast_weather(28.6139, 77.2090, "delhi", days=5)
    assert len(forecast) == 5
    assert forecast[0]["horizon_day"] == 1
    assert "temp_c" in forecast[0]


def test_open_meteo_hourly_forecast():
    """Verify 24-hour hourly live forecast from Open-Meteo."""
    provider = OpenMeteoProvider()
    hourly = provider.get_hourly_forecast(19.0760, 72.8777, "mumbai", hours=24)
    assert len(hourly) >= 1
    first_hour = hourly[0]
    assert "temp_c" in first_hour
    assert "utci_c" in first_hour
    assert "wbgt_c" in first_hour
    assert "hazard_score" in first_hour


def test_nominatim_reverse_geocoder():
    """Verify OpenStreetMap Nominatim reverse geocoder returns human-readable location."""
    geocoder = NominatimGeocoder()
    res = geocoder.reverse_geocode(23.0225, 72.5714)
    assert "city" in res
    assert "country" in res
    assert "display_name" in res


def test_live_weather_and_risk_endpoints():
    """Verify live API endpoints accepting custom lat/lon."""
    # 1. Reverse Geocode endpoint
    res_geo = client.get("/api/v1/geocode/reverse?lat=23.0225&lon=72.5714")
    assert res_geo.status_code == 200
    assert "city" in res_geo.json()

    # 2. Live Current Weather endpoint
    res_w = client.get("/api/v1/weather/current?lat=23.0225&lon=72.5714")
    assert res_w.status_code == 200
    data_w = res_w.json()
    assert "weather" in data_w
    assert "temp_c" in data_w["weather"]

    # 3. Live Hourly Weather endpoint
    res_h = client.get("/api/v1/weather/hourly?lat=23.0225&lon=72.5714&hours=24")
    assert res_h.status_code == 200
    data_h = res_h.json()
    assert "hourly_series" in data_h

    # 4. Live Thermal endpoint
    res_th = client.get("/api/v1/thermal/current?lat=23.0225&lon=72.5714")
    assert res_th.status_code == 200
    data_th = res_th.json()
    assert "thermal_analysis" in data_th
    assert "utci" in data_th["thermal_analysis"]["metrics"]

    # 5. Live Risk endpoint
    res_r = client.get("/api/v1/risk/current?lat=23.0225&lon=72.5714")
    assert res_r.status_code == 200
    data_r = res_r.json()
    assert "heat_risk_score" in data_r
    assert "alert_level" in data_r

    # 6. Live Map endpoint with custom lat/lon
    res_map = client.get("/api/v1/map/risk?lat=19.0760&lon=72.8777&day=1") # Mumbai
    assert res_map.status_code == 200
    data_map = res_map.json()
    assert data_map["type"] == "FeatureCollection"
    assert len(data_map["features"]) >= 1
