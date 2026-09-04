"""
NASA POWER API Meteorological Ingestion Adapter.

Fetches analysis-ready surface meteorology and solar irradiance parameters from
the NASA Langley Research Center POWER API (Prediction Of Worldwide Energy Resources).
"""

import requests
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta, timezone
from .base import WeatherProvider
from .cache import DataCache


class NASAPowerProvider(WeatherProvider):
    """
    Client for NASA POWER Daily Point API with caching and deterministic fallback fixtures.
    """

    BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
    COMMUNITY = "RE"
    PARAMETERS = "T2M,RH2M,WS10M,WS2M,ALLSKY_SFC_SW_DWN"

    def __init__(
        self,
        cache: Optional[DataCache] = None,
        demo_mode: bool = True,
        timeout_seconds: int = 10
    ):
        self.cache = cache or DataCache()
        self.demo_mode = demo_mode
        self.timeout = timeout_seconds

    def _get_demo_forecast(self, city_id: str, days: int = 5) -> List[Dict[str, Any]]:
        """
        Deterministic, realistic pre-monsoon heatwave scenarios for Indian pilot cities.
        Simulates escalating heatwave conditions over a 5-day horizon.
        """
        # Climatological summer base for Ahmedabad:
        # Day 1: Hot & moderate RH
        # Day 2: Increasing Temp & Solar
        # Day 3: Peak Heatwave (Extreme)
        # Day 4: High Temp + Higher Humidity (Severe Physiological Strain)
        # Day 5: Sustained Heatwave
        city_profiles = {
            "ahmedabad": [
                {"day": 1, "temp_c": 41.2, "rh_pct": 28.0, "wind_10m": 3.2, "solar_w_m2": 680.0, "desc": "Sunny & Dry"},
                {"day": 2, "temp_c": 42.8, "rh_pct": 32.0, "wind_10m": 2.6, "solar_w_m2": 720.0, "desc": "Heatwave Warning"},
                {"day": 3, "temp_c": 44.5, "rh_pct": 38.0, "wind_10m": 1.8, "solar_w_m2": 780.0, "desc": "Severe Heatwave Peak"},
                {"day": 4, "temp_c": 43.6, "rh_pct": 48.0, "wind_10m": 1.2, "solar_w_m2": 750.0, "desc": "Humid Extreme Stress"},
                {"day": 5, "temp_c": 42.0, "rh_pct": 52.0, "wind_10m": 2.1, "solar_w_m2": 690.0, "desc": "Sustained Heatwave"}
            ],
            "delhi": [
                {"day": 1, "temp_c": 39.5, "rh_pct": 25.0, "wind_10m": 3.8, "solar_w_m2": 650.0, "desc": "Clear Skies"},
                {"day": 2, "temp_c": 41.0, "rh_pct": 30.0, "wind_10m": 2.9, "solar_w_m2": 700.0, "desc": "Moderate Heat"},
                {"day": 3, "temp_c": 43.2, "rh_pct": 35.0, "wind_10m": 2.0, "solar_w_m2": 740.0, "desc": "Heatwave Warning"},
                {"day": 4, "temp_c": 44.0, "rh_pct": 40.0, "wind_10m": 1.5, "solar_w_m2": 760.0, "desc": "Peak Heat Stress"},
                {"day": 5, "temp_c": 42.5, "rh_pct": 45.0, "wind_10m": 2.4, "solar_w_m2": 710.0, "desc": "Persistent Heat"}
            ]
        }
        raw_series = city_profiles.get(city_id.lower(), city_profiles["ahmedabad"])
        
        now = datetime.now(timezone.utc)
        result = []
        for i in range(min(days, len(raw_series))):
            item = raw_series[i]
            target_date = now + timedelta(days=i)
            result.append({
                "horizon_day": item["day"],
                "horizon_label": f"D+{item['day']-1}" if item["day"] > 1 else "Current (D+0)",
                "date": target_date.strftime("%Y-%m-%d"),
                "temp_c": item["temp_c"],
                "relative_humidity_pct": item["rh_pct"],
                "wind_speed_10m_m_s": item["wind_10m"],
                "solar_radiation_w_m2": item["solar_w_m2"],
                "condition_summary": item["desc"],
                "provider": "NASA_POWER (Curated Demo Fixture)",
                "is_demo_data": True
            })
        return result

    def get_current_weather(self, lat: float, lon: float, city_id: str = "ahmedabad") -> Dict[str, Any]:
        """Fetch current day meteorological parameters."""
        forecast = self.get_forecast_weather(lat, lon, city_id, days=1)
        if forecast:
            return forecast[0]
        # Fallback
        return {
            "temp_c": 41.0,
            "relative_humidity_pct": 30.0,
            "wind_speed_10m_m_s": 2.5,
            "solar_radiation_w_m2": 700.0,
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "provider": "Fallback",
            "is_demo_data": True
        }

    def get_forecast_weather(
        self,
        lat: float,
        lon: float,
        city_id: str = "ahmedabad",
        days: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Fetch 5-day daily meteorological series.
        Checks cache first, then attempts live NASA POWER API, falling back to demo fixtures.
        """
        cache_params = {"lat": round(lat, 4), "lon": round(lon, 4), "days": days, "city": city_id}
        
        # 1. In demo mode or if cached, return instantly
        if self.demo_mode:
            return self._get_demo_forecast(city_id, days)

        cached = self.cache.get("nasa_power_forecast", cache_params)
        if cached:
            return cached

        # 2. Attempt Live API Fetch from NASA POWER
        try:
            end_dt = datetime.now(timezone.utc)
            start_dt = end_dt - timedelta(days=7) # NASA POWER daily analysis has a 2-3 day latency
            
            params = {
                "parameters": self.PARAMETERS,
                "community": self.COMMUNITY,
                "longitude": lon,
                "latitude": lat,
                "start": start_dt.strftime("%Y%m%d"),
                "end": end_dt.strftime("%Y%m%d"),
                "format": "JSON"
            }
            
            response = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                properties = data.get("properties", {}).get("parameter", {})
                
                t2m = properties.get("T2M", {})
                rh2m = properties.get("RH2M", {})
                ws10m = properties.get("WS10M", {})
                solar_raw = properties.get("ALLSKY_SFC_SW_DWN", {})
                
                # Extract most recent dates
                valid_dates = sorted(t2m.keys())
                if valid_dates:
                    results = []
                    for idx, d_str in enumerate(valid_dates[-days:]):
                        t_val = float(t2m.get(d_str, 40.0))
                        rh_val = float(rh2m.get(d_str, 35.0))
                        ws_val = float(ws10m.get(d_str, 2.0))
                        # Solar MJ/m2/day to approx peak W/m2: S_peak ~ (MJ * 10^6) / (12*3600 * 2/pi) ~ MJ * 36.4
                        solar_mj = float(solar_raw.get(d_str, 20.0))
                        solar_w_m2 = max(0.0, solar_mj * 36.4) if solar_mj > 0 else 600.0

                        results.append({
                            "horizon_day": idx + 1,
                            "horizon_label": f"D+{idx}",
                            "date": d_str,
                            "temp_c": round(t_val, 1),
                            "relative_humidity_pct": round(rh_val, 1),
                            "wind_speed_10m_m_s": round(ws_val, 1),
                            "solar_radiation_w_m2": round(solar_w_m2, 1),
                            "provider": "NASA_POWER (Live API)",
                            "is_demo_data": False
                        })
                    
                    self.cache.set("nasa_power_forecast", cache_params, results)
                    return results
        except Exception:
            # On network timeout or rate limit, fall back safely to curated demo data
            pass

        demo_data = self._get_demo_forecast(city_id, days)
        self.cache.set("nasa_power_forecast", cache_params, demo_data)
        return demo_data
