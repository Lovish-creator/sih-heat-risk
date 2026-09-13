"""
Unit and Integration Tests for Real Live Open Data APIs (Open-Meteo & OpenStreetMap Nominatim).
Deterministic with mocks for offline/CI reproducibility.
"""

import sys
import os
from unittest.mock import patch, MagicMock
import requests
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.main import app
from backend.app.data_sources.open_meteo import OpenMeteoProvider
from backend.app.data_sources.geocoding import NominatimGeocoder

client = TestClient(app)


def _mock_open_meteo_response(*args, **kwargs):
    mock = MagicMock()
    mock.status_code = 200
    params = kwargs.get("params", {})
    
    if "current" in params:
        mock.json.return_value = {
            "elevation": 50,
            "current": {
                "time": "2026-06-15T12:00",
                "temperature_2m": 38.5,
                "relative_humidity_2m": 45.0,
                "apparent_temperature": 42.0,
                "dew_point_2m": 24.5,
                "surface_pressure": 1008.0,
                "cloud_cover": 15.0,
                "wind_speed_10m": 12.6,
                "wind_direction_10m": 240.0,
                "wind_gusts_10m": 18.0,
                "shortwave_radiation": 650.0,
                "direct_normal_irradiance": 500.0,
                "diffuse_radiation": 150.0,
                "uv_index": 8.0,
                "is_day": 1,
                "precipitation": 0.0
            }
        }
    elif "daily" in params:
        mock.json.return_value = {
            "daily": {
                "time": ["2026-06-15", "2026-06-16", "2026-06-17", "2026-06-18", "2026-06-19"],
                "temperature_2m_max": [39.0, 40.5, 41.0, 39.5, 38.0],
                "temperature_2m_min": [26.0, 27.0, 28.0, 27.0, 26.0],
                "relative_humidity_2m_mean": [45.0, 42.0, 40.0, 48.0, 50.0],
                "wind_speed_10m_max": [14.0, 15.0, 12.0, 10.0, 11.0],
                "shortwave_radiation_sum": [22.0, 23.0, 24.0, 21.0, 20.0],
                "uv_index_max": [9.0, 9.5, 10.0, 8.5, 8.0],
                "precipitation_sum": [0.0, 0.0, 0.0, 0.0, 0.0]
            }
        }
    elif "hourly" in params:
        times = [f"2026-06-15T{h:02d}:00" for h in range(24)] + [f"2026-06-16T{h:02d}:00" for h in range(24)]
        mock.json.return_value = {
            "hourly": {
                "time": times,
                "temperature_2m": [30.0 + (i % 10) for i in range(48)],
                "relative_humidity_2m": [50.0 for _ in range(48)],
                "dew_point_2m": [20.0 for _ in range(48)],
                "surface_pressure": [1010.0 for _ in range(48)],
                "cloud_cover": [10.0 for _ in range(48)],
                "wind_speed_10m": [8.0 for _ in range(48)],
                "wind_direction_10m": [220.0 for _ in range(48)],
                "wind_gusts_10m": [12.0 for _ in range(48)],
                "shortwave_radiation": [500.0 for _ in range(48)],
                "direct_normal_irradiance": [400.0 for _ in range(48)],
                "uv_index": [5.0 for _ in range(48)]
            }
        }
    else:
        mock.json.return_value = {}
    return mock


def _get_mock_provider():
    mock_cache = MagicMock()
    mock_cache.get.return_value = None
    return OpenMeteoProvider(cache=mock_cache)


@patch("requests.get", side_effect=_mock_open_meteo_response)
def test_open_meteo_provider_mocked(mock_get):
    """Verify Open-Meteo provider parses API response into standard meteorological variables."""
    provider = _get_mock_provider()
    current = provider.get_current_weather(23.0225, 72.5714, "ahmedabad")
    assert "temp_c" in current
    assert current["temp_c"] == 38.5
    assert current["relative_humidity_pct"] == 45.0
    assert current["wind_speed_10m_m_s"] == 3.5  # 12.6 km/h / 3.6
    assert current["solar_radiation_w_m2"] == 650.0
    assert not current["is_demo_data"]


@patch("requests.get", side_effect=_mock_open_meteo_response)
def test_open_meteo_forecast_mocked(mock_get):
    """Verify multi-day forecast retrieval from Open-Meteo with mocked stream."""
    provider = _get_mock_provider()
    forecast = provider.get_forecast_weather(28.6139, 77.2090, "delhi", days=5)
    assert len(forecast) == 5
    assert forecast[0]["horizon_day"] == 1
    assert forecast[0]["temp_c"] == 39.0
    assert forecast[1]["temp_c"] == 40.5


@patch("requests.get", side_effect=_mock_open_meteo_response)
def test_open_meteo_hourly_forecast_mocked(mock_get):
    """Verify 24-hour hourly forecast with biometeorology computation."""
    provider = _get_mock_provider()
    hourly = provider.get_hourly_forecast(19.0760, 72.8777, "mumbai", hours=24)
    assert len(hourly) == 24
    first_hour = hourly[0]
    assert "temp_c" in first_hour
    assert "utci_c" in first_hour
    assert "wbgt_c" in first_hour
    assert "hazard_score" in first_hour


@patch("requests.get", side_effect=requests.RequestException("Simulated upstream network timeout"))
def test_open_meteo_deterministic_fallbacks_on_failure(mock_get):
    """Verify provider returns valid deterministic fallbacks on upstream network error."""
    provider = _get_mock_provider()
    # 1. Current weather fallback
    curr_fb = provider.get_current_weather(23.0225, 72.5714, "fallback_test")
    assert curr_fb["is_demo_data"] is True
    assert "temp_c" in curr_fb
    assert curr_fb["temp_c"] > 0

    # 2. Forecast fallback
    fc_fb = provider.get_forecast_weather(23.0225, 72.5714, "fallback_test", days=5)
    assert len(fc_fb) == 5
    assert fc_fb[0]["is_demo_data"] is True
    assert "temp_c" in fc_fb[0]

    # 3. Hourly fallback
    hr_fb = provider.get_hourly_forecast(23.0225, 72.5714, "fallback_test", hours=24)
    assert len(hr_fb) == 24
    assert "utci_c" in hr_fb[0]


def test_nominatim_reverse_geocoder():
    """Verify OpenStreetMap Nominatim reverse geocoder returns human-readable location."""
    geocoder = NominatimGeocoder()
    res = geocoder.reverse_geocode(23.0225, 72.5714)
    assert "city" in res
    assert "country" in res
    assert "display_name" in res


def test_live_weather_and_risk_endpoints():
    """Verify API endpoints accepting custom lat/lon."""
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
    res_map = client.get("/api/v1/map/risk?lat=19.0760&lon=72.8777&day=1")
    assert res_map.status_code == 200
    data_map = res_map.json()
    assert data_map["type"] == "FeatureCollection"
    assert len(data_map["features"]) >= 1
