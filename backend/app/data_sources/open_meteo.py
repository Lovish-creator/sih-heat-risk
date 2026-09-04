"""
Open-Meteo Real-Time & Forecast Meteorological Ingestion Adapter.

Fetches live real-time surface meteorology and solar radiation parameters
from the open, free Open-Meteo Weather API (https://open-meteo.com/).
No API keys required.
"""

import requests
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta
from .base import WeatherProvider
from .cache import DataCache


class OpenMeteoProvider(WeatherProvider):
    """
    Client for Open-Meteo live API with automatic caching and solar flux conversion.
    """

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, cache: Optional[DataCache] = None, timeout_seconds: int = 10):
        self.cache = cache or DataCache(default_ttl_seconds=900)  # 15 min cache for live data
        self.timeout = timeout_seconds

    def get_current_weather(self, lat: float, lon: float, city_id: str = "custom") -> Dict[str, Any]:
        """
        Fetch real-time live current weather for any latitude and longitude.
        """
        cache_key = {"lat": round(lat, 4), "lon": round(lon, 4), "mode": "current"}
        cached = self.cache.get("open_meteo_current", cache_key)
        if cached:
            return cached

        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "direct_normal_irradiance", "shortwave_radiation"],
            "timezone": "auto"
        }

        try:
            res = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
            if res.status_code == 200:
                data = res.json()
                curr = data.get("current", {})
                
                temp_c = float(curr.get("temperature_2m", 30.0))
                rh = float(curr.get("relative_humidity_2m", 50.0))
                ws = float(curr.get("wind_speed_10m", 2.0))
                
                # Wind in Open-Meteo defaults to km/h if not specified; let's check or convert to m/s
                # Open-Meteo default wind_speed_10m is km/h -> convert to m/s: km/h / 3.6
                ws_ms = round(ws / 3.6, 1) if ws > 0 else 1.0
                
                # Solar radiation: shortwave_radiation or direct_normal_irradiance in W/m^2
                solar_w_m2 = float(curr.get("shortwave_radiation", curr.get("direct_normal_irradiance", 0.0)))
                if solar_w_m2 < 0:
                    solar_w_m2 = 0.0

                result = {
                    "temp_c": round(temp_c, 1),
                    "relative_humidity_pct": round(rh, 1),
                    "wind_speed_10m_m_s": max(0.5, ws_ms),
                    "solar_radiation_w_m2": round(solar_w_m2, 1),
                    "timestamp": curr.get("time", datetime.now(timezone.utc).isoformat()),
                    "date": curr.get("time", "")[:10] if curr.get("time") else datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "provider": "Open-Meteo (Live Real-Time Stream)",
                    "is_demo_data": False,
                    "latitude": lat,
                    "longitude": lon
                }
                self.cache.set("open_meteo_current", cache_key, result, ttl_seconds=900)
                return result
        except Exception as e:
            # Fallback on network failure
            pass

        return {
            "temp_c": 32.0,
            "relative_humidity_pct": 55.0,
            "wind_speed_10m_m_s": 2.2,
            "solar_radiation_w_m2": 450.0,
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "provider": "Open-Meteo Fallback",
            "is_demo_data": True,
            "latitude": lat,
            "longitude": lon
        }

    def get_forecast_weather(
        self,
        lat: float,
        lon: float,
        city_id: str = "custom",
        days: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Fetch real-time 5-7 day multi-horizon forecast for any coordinates.
        """
        cache_key = {"lat": round(lat, 4), "lon": round(lon, 4), "days": days, "mode": "forecast"}
        cached = self.cache.get("open_meteo_forecast", cache_key)
        if cached:
            return cached

        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ["temperature_2m_max", "relative_humidity_2m_mean", "wind_speed_10m_max", "shortwave_radiation_sum"],
            "timezone": "auto",
            "forecast_days": min(7, max(1, days))
        }

        try:
            res = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
            if res.status_code == 200:
                data = res.json()
                daily = data.get("daily", {})
                
                dates = daily.get("time", [])
                temps = daily.get("temperature_2m_max", [])
                rhs = daily.get("relative_humidity_2m_mean", [])
                winds = daily.get("wind_speed_10m_max", [])
                solars = daily.get("shortwave_radiation_sum", [])

                results = []
                for i in range(min(days, len(dates))):
                    t_val = float(temps[i]) if i < len(temps) and temps[i] is not None else 32.0
                    rh_val = float(rhs[i]) if i < len(rhs) and rhs[i] is not None else 50.0
                    
                    # Convert wind speed km/h to m/s
                    w_kmh = float(winds[i]) if i < len(winds) and winds[i] is not None else 8.0
                    ws_ms = max(0.5, round(w_kmh / 3.6, 1))

                    # Solar radiation sum in MJ/m^2 -> convert to approximate peak daytime irradiance (W/m^2)
                    solar_mj = float(solars[i]) if i < len(solars) and solars[i] is not None else 18.0
                    solar_w_m2 = max(0.0, round(solar_mj * 36.4, 1))

                    results.append({
                        "horizon_day": i + 1,
                        "horizon_label": f"D+{i}" if i > 0 else "Current (D+0)",
                        "date": dates[i],
                        "temp_c": round(t_val, 1),
                        "relative_humidity_pct": round(rh_val, 1),
                        "wind_speed_10m_m_s": ws_ms,
                        "solar_radiation_w_m2": solar_w_m2,
                        "provider": "Open-Meteo (Live Real-Time Forecast)",
                        "is_demo_data": False,
                        "latitude": lat,
                        "longitude": lon
                    })

                self.cache.set("open_meteo_forecast", cache_key, results, ttl_seconds=1800)
                return results
        except Exception as e:
            pass

        # Return fallback on network error
        return [
            {
                "horizon_day": 1,
                "horizon_label": "Current (D+0)",
                "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "temp_c": 33.0,
                "relative_humidity_pct": 52.0,
                "wind_speed_10m_m_s": 2.0,
                "solar_radiation_w_m2": 600.0,
                "provider": "Fallback",
                "is_demo_data": True,
                "latitude": lat,
                "longitude": lon
            }
        ]
