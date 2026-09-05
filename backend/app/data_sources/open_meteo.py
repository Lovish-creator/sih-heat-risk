"""
Open-Meteo Real-Time & Forecast Meteorological Ingestion Adapter.

Fetches live real-time surface meteorology, hourly forecasts, and solar irradiance
from the Open-Meteo Weather API (https://open-meteo.com/).
100% Free & Open (Zero API Keys Required).
"""

import requests
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta
from .base import WeatherProvider
from .cache import DataCache
from ..thermal.hazard import calculate_thermal_hazard


def wind_deg_to_compass(deg: float) -> str:
    """Convert meteorological wind direction in degrees to 16-point compass label."""
    if deg is None:
        return "N/A"
    val = int((deg / 22.5) + 0.5)
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return directions[(val % 16)]


class OpenMeteoProvider(WeatherProvider):
    """
    Client for Open-Meteo live API with automatic caching, hourly biometeorology, and solar flux conversion.
    """

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, cache: Optional[DataCache] = None, timeout_seconds: int = 10):
        self.cache = cache or DataCache(default_ttl_seconds=600)  # 10 min cache for live data
        self.timeout = timeout_seconds

    def get_current_weather(self, lat: float, lon: float, city_id: str = "custom") -> Dict[str, Any]:
        """
        Fetch real-time live current weather for any latitude and longitude.
        """
        cache_key = {"lat": round(lat, 4), "lon": round(lon, 4), "mode": "current_live"}
        cached = self.cache.get("open_meteo_current", cache_key)
        if cached:
            return cached

        params = {
            "latitude": lat,
            "longitude": lon,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "dew_point_2m",
                "surface_pressure",
                "cloud_cover",
                "wind_speed_10m",
                "wind_direction_10m",
                "wind_gusts_10m",
                "shortwave_radiation",
                "direct_normal_irradiance",
                "diffuse_radiation",
                "uv_index",
                "is_day",
                "precipitation"
            ],
            "timezone": "auto"
        }

        try:
            res = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
            if res.status_code == 200:
                data = res.json()
                curr = data.get("current", {})
                
                temp_c = float(curr.get("temperature_2m", 30.0))
                rh = float(curr.get("relative_humidity_2m", 50.0))
                ws_kmh = float(curr.get("wind_speed_10m", 7.2))
                wind_dir = float(curr.get("wind_direction_10m", 0.0))
                wind_gust = float(curr.get("wind_gusts_10m", ws_kmh * 1.3))
                dew_point = float(curr.get("dew_point_2m", temp_c - ((100.0 - rh) / 5.0)))
                pressure = float(curr.get("surface_pressure", 1010.0))
                cloud = float(curr.get("cloud_cover", 0.0))
                uv = float(curr.get("uv_index", 0.0))
                
                # Convert wind speed km/h -> m/s: ws_ms = ws_kmh / 3.6
                ws_ms = max(0.5, round(ws_kmh / 3.6, 1))
                
                # Solar radiation in W/m^2
                solar_w_m2 = max(0.0, float(curr.get("shortwave_radiation", curr.get("direct_normal_irradiance", 0.0))))
                direct_dni = max(0.0, float(curr.get("direct_normal_irradiance", 0.0)))
                diffuse_w = max(0.0, float(curr.get("diffuse_radiation", 0.0)))

                # Magnus-Tetens Water Vapor Pressure (hPa)
                es = 6.112 * (2.718281828459045 ** ((17.67 * temp_c) / (temp_c + 243.5)))
                vapor_pres = round(es * (rh / 100.0), 2)
                
                obs_time = curr.get("time", datetime.now(timezone.utc).isoformat())

                result = {
                    "temp_c": round(temp_c, 1),
                    "relative_humidity_pct": round(rh, 1),
                    "apparent_temperature_c": round(float(curr.get("apparent_temperature", temp_c)), 1),
                    "dew_point_c": round(dew_point, 1),
                    "surface_pressure_hpa": round(pressure, 1),
                    "cloud_cover_pct": round(cloud, 0),
                    "wind_speed_10m_m_s": ws_ms,
                    "wind_speed_kmh": round(ws_kmh, 1),
                    "wind_gusts_kmh": round(wind_gust, 1),
                    "wind_direction_deg": round(wind_dir, 0),
                    "wind_direction_compass": wind_deg_to_compass(wind_dir),
                    "solar_radiation_w_m2": round(solar_w_m2, 1),
                    "direct_normal_irradiance_w_m2": round(direct_dni, 1),
                    "diffuse_radiation_w_m2": round(diffuse_w, 1),
                    "uv_index": round(uv, 1),
                    "vapor_pressure_hpa": vapor_pres,
                    "is_day": bool(curr.get("is_day", 1)),
                    "precipitation_mm": float(curr.get("precipitation", 0.0)),
                    "timestamp": obs_time,
                    "date": obs_time[:10] if obs_time else datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "provider": "Open-Meteo Live High-Resolution API",
                    "is_demo_data": False,
                    "latitude": lat,
                    "longitude": lon,
                    "elevation_m": data.get("elevation", 0)
                }
                self.cache.set("open_meteo_current", cache_key, result, ttl_seconds=600)
                return result
        except Exception:
            pass

        return {
            "temp_c": 30.0,
            "relative_humidity_pct": 55.0,
            "apparent_temperature_c": 32.0,
            "dew_point_c": 20.0,
            "surface_pressure_hpa": 1010.0,
            "cloud_cover_pct": 10.0,
            "wind_speed_10m_m_s": 2.0,
            "wind_speed_kmh": 7.2,
            "wind_gusts_kmh": 10.0,
            "wind_direction_deg": 225.0,
            "wind_direction_compass": "SW",
            "solar_radiation_w_m2": 450.0,
            "direct_normal_irradiance_w_m2": 350.0,
            "diffuse_radiation_w_m2": 100.0,
            "uv_index": 5.0,
            "vapor_pressure_hpa": 23.3,
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "provider": "Open-Meteo Live (Fallback)",
            "is_demo_data": True,
            "latitude": lat,
            "longitude": lon
        }

    def get_hourly_forecast(
        self,
        lat: float,
        lon: float,
        city_id: str = "custom",
        hours: int = 24
    ) -> List[Dict[str, Any]]:
        """
        Fetch live hourly meteorological series for the next 24 hours with computed biometeorology.
        """
        cache_key = {"lat": round(lat, 4), "lon": round(lon, 4), "hours": hours, "mode": "hourly_live"}
        cached = self.cache.get("open_meteo_hourly", cache_key)
        if cached:
            return cached

        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "dew_point_2m",
                "surface_pressure",
                "cloud_cover",
                "wind_speed_10m",
                "wind_direction_10m",
                "wind_gusts_10m",
                "shortwave_radiation",
                "direct_normal_irradiance",
                "uv_index"
            ],
            "timezone": "auto",
            "forecast_days": 2
        }

        try:
            res = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
            if res.status_code == 200:
                data = res.json()
                hourly = data.get("hourly", {})
                
                times = hourly.get("time", [])
                temps = hourly.get("temperature_2m", [])
                rhs = hourly.get("relative_humidity_2m", [])
                dews = hourly.get("dew_point_2m", [])
                pressures = hourly.get("surface_pressure", [])
                clouds = hourly.get("cloud_cover", [])
                winds = hourly.get("wind_speed_10m", [])
                wind_dirs = hourly.get("wind_direction_10m", [])
                gusts = hourly.get("wind_gusts_10m", [])
                solars = hourly.get("shortwave_radiation", [])
                uvs = hourly.get("uv_index", [])

                # Find current hour index
                now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:00")
                start_idx = 0
                for idx, t_str in enumerate(times):
                    if t_str >= now_iso:
                        start_idx = idx
                        break

                results = []
                for i in range(start_idx, min(start_idx + hours, len(times))):
                    t_val = float(temps[i]) if i < len(temps) and temps[i] is not None else 30.0
                    rh_val = float(rhs[i]) if i < len(rhs) and rhs[i] is not None else 50.0
                    dew_val = float(dews[i]) if i < len(dews) and dews[i] is not None else round(t_val - ((100.0 - rh_val)/5.0), 1)
                    press_val = float(pressures[i]) if i < len(pressures) and pressures[i] is not None else 1010.0
                    cloud_val = float(clouds[i]) if i < len(clouds) and clouds[i] is not None else 0.0
                    w_kmh = float(winds[i]) if i < len(winds) and winds[i] is not None else 7.2
                    w_dir = float(wind_dirs[i]) if i < len(wind_dirs) and wind_dirs[i] is not None else 0.0
                    w_gust = float(gusts[i]) if i < len(gusts) and gusts[i] is not None else (w_kmh * 1.3)
                    ws_ms = max(0.5, round(w_kmh / 3.6, 1))
                    solar_val = max(0.0, float(solars[i])) if i < len(solars) and solars[i] is not None else 0.0
                    uv_val = float(uvs[i]) if i < len(uvs) and uvs[i] is not None else 0.0

                    # Compute real-time biometeorological hazard for this specific hour
                    hz = calculate_thermal_hazard(
                        temp_c=t_val,
                        relative_humidity_pct=rh_val,
                        wind_speed_10m_m_s=ws_ms,
                        solar_radiation_w_m2=solar_val
                    )

                    time_label = times[i][11:16] if len(times[i]) >= 16 else times[i]

                    results.append({
                        "hour_index": len(results) + 1,
                        "time_iso": times[i],
                        "hour_label": time_label,
                        "date": times[i][:10],
                        "temp_c": round(t_val, 1),
                        "relative_humidity_pct": round(rh_val, 1),
                        "dew_point_c": round(dew_val, 1),
                        "surface_pressure_hpa": round(press_val, 1),
                        "cloud_cover_pct": round(cloud_val, 0),
                        "wind_speed_10m_m_s": ws_ms,
                        "wind_speed_kmh": round(w_kmh, 1),
                        "wind_gusts_kmh": round(w_gust, 1),
                        "wind_direction_deg": round(w_dir, 0),
                        "wind_direction_compass": wind_deg_to_compass(w_dir),
                        "solar_radiation_w_m2": round(solar_val, 1),
                        "uv_index": round(uv_val, 1),
                        "utci_c": hz["metrics"]["utci"]["value_c"],
                        "utci_category": hz["metrics"]["utci"]["category"],
                        "wbgt_c": hz["metrics"]["wbgt"]["value_c"],
                        "wbgt_risk": hz["metrics"]["wbgt"]["risk_level"],
                        "heat_index_c": hz["metrics"]["heat_index"]["value_c"],
                        "hazard_score": hz["composite_hazard_score"]
                    })

                self.cache.set("open_meteo_hourly", cache_key, results, ttl_seconds=600)
                return results
        except Exception:
            pass

        # Return structured fallback if network fails
        return []

    def get_forecast_weather(
        self,
        lat: float,
        lon: float,
        city_id: str = "custom",
        days: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Fetch real-time 5-7 day multi-horizon forecast for any coordinates.
        """
        cache_key = {"lat": round(lat, 4), "lon": round(lon, 4), "days": days, "mode": "forecast_live"}
        cached = self.cache.get("open_meteo_forecast", cache_key)
        if cached:
            return cached

        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "relative_humidity_2m_mean",
                "wind_speed_10m_max",
                "shortwave_radiation_sum",
                "uv_index_max",
                "precipitation_sum"
            ],
            "timezone": "auto",
            "forecast_days": min(7, max(1, days))
        }

        try:
            res = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
            if res.status_code == 200:
                data = res.json()
                daily = data.get("daily", {})
                
                dates = daily.get("time", [])
                temps_max = daily.get("temperature_2m_max", [])
                temps_min = daily.get("temperature_2m_min", [])
                rhs = daily.get("relative_humidity_2m_mean", [])
                winds = daily.get("wind_speed_10m_max", [])
                solars = daily.get("shortwave_radiation_sum", [])
                uvs = daily.get("uv_index_max", [])
                precips = daily.get("precipitation_sum", [])

                results = []
                for i in range(min(days, len(dates))):
                    t_max = float(temps_max[i]) if i < len(temps_max) and temps_max[i] is not None else 32.0
                    t_min = float(temps_min[i]) if i < len(temps_min) and temps_min[i] is not None else 24.0
                    rh_val = float(rhs[i]) if i < len(rhs) and rhs[i] is not None else 50.0
                    
                    w_kmh = float(winds[i]) if i < len(winds) and winds[i] is not None else 8.0
                    ws_ms = max(0.5, round(w_kmh / 3.6, 1))

                    # Solar radiation sum in MJ/m^2 -> convert to approximate peak daytime irradiance (W/m^2)
                    solar_mj = float(solars[i]) if i < len(solars) and solars[i] is not None else 18.0
                    solar_w_m2 = max(0.0, round(solar_mj * 36.4, 1))
                    
                    uv_val = float(uvs[i]) if i < len(uvs) and uvs[i] is not None else 6.0
                    precip_val = float(precips[i]) if i < len(precips) and precips[i] is not None else 0.0

                    results.append({
                        "horizon_day": i + 1,
                        "horizon_label": f"D+{i}" if i > 0 else "Today (D+0)",
                        "date": dates[i],
                        "temp_c": round(t_max, 1),
                        "temp_min_c": round(t_min, 1),
                        "relative_humidity_pct": round(rh_val, 1),
                        "wind_speed_10m_m_s": ws_ms,
                        "wind_speed_kmh": round(w_kmh, 1),
                        "solar_radiation_w_m2": solar_w_m2,
                        "uv_index": round(uv_val, 1),
                        "precipitation_mm": round(precip_val, 1),
                        "provider": "Open-Meteo (Live Forecast Stream)",
                        "is_demo_data": False,
                        "latitude": lat,
                        "longitude": lon
                    })

                self.cache.set("open_meteo_forecast", cache_key, results, ttl_seconds=1800)
                return results
        except Exception:
            pass

        return []
