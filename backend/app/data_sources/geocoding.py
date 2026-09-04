"""
OpenStreetMap Nominatim Geocoding & Reverse Geocoding Adapter.

Resolves geographic coordinates (lat/lon) into human-readable address hierarchies
(ward, suburb, city, district, state, country) and allows searching any global location.
Zero API keys required (Open Data / OpenStreetMap).
"""

import requests
import time
from typing import Dict, Any, List, Optional
from .cache import DataCache


class NominatimGeocoder:
    """
    Client for OpenStreetMap Nominatim API with caching and polite request handling.
    """

    REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"
    SEARCH_URL = "https://nominatim.openstreetmap.org/search"
    USER_AGENT = "SIH26083-ThermoShield-Heat-Risk-Early-Warning/1.0"

    def __init__(self, cache: Optional[DataCache] = None, timeout_seconds: int = 8):
        self.cache = cache or DataCache(default_ttl_seconds=86400) # 24h cache for geocoding
        self.timeout = timeout_seconds

    def reverse_geocode(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Convert latitude and longitude into administrative address details.
        """
        cache_key = {"lat": round(lat, 4), "lon": round(lon, 4), "type": "reverse"}
        cached = self.cache.get("nominatim_reverse", cache_key)
        if cached:
            return cached

        headers = {"User-Agent": self.USER_AGENT}
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json",
            "addressdetails": 1,
            "zoom": 14
        }

        try:
            res = requests.get(self.REVERSE_URL, params=params, headers=headers, timeout=self.timeout)
            if res.status_code == 200:
                data = res.json()
                address = data.get("address", {})
                
                city = address.get("city") or address.get("town") or address.get("village") or address.get("municipality") or address.get("county") or "Detected Location"
                suburb = address.get("suburb") or address.get("neighbourhood") or address.get("residential") or address.get("ward") or ""
                state = address.get("state") or address.get("state_district") or ""
                country = address.get("country") or "India"

                result = {
                    "display_name": data.get("display_name", f"{lat:.4f}, {lon:.4f}"),
                    "city": city,
                    "suburb_or_ward": suburb,
                    "state": state,
                    "country": country,
                    "latitude": lat,
                    "longitude": lon,
                    "raw_address": address,
                    "source": "OpenStreetMap Nominatim API"
                }
                self.cache.set("nominatim_reverse", cache_key, result)
                return result
        except Exception:
            pass

        return {
            "display_name": f"Location ({lat:.4f}, {lon:.4f})",
            "city": "Current Location",
            "suburb_or_ward": "",
            "state": "",
            "country": "India",
            "latitude": lat,
            "longitude": lon,
            "source": "Fallback Geocoder"
        }

    def search_locations(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for locations / cities by name.
        """
        q_clean = query.strip()
        if not q_clean:
            return []

        cache_key = {"q": q_clean.lower(), "limit": limit, "type": "search"}
        cached = self.cache.get("nominatim_search", cache_key)
        if cached:
            return cached

        headers = {"User-Agent": self.USER_AGENT}
        params = {
            "q": q_clean,
            "format": "json",
            "addressdetails": 1,
            "limit": limit
        }

        try:
            res = requests.get(self.SEARCH_URL, params=params, headers=headers, timeout=self.timeout)
            if res.status_code == 200:
                items = res.json()
                results = []
                for item in items:
                    addr = item.get("address", {})
                    city = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("county") or item.get("name", "Unknown")
                    results.append({
                        "name": item.get("display_name"),
                        "city": city,
                        "state": addr.get("state", ""),
                        "country": addr.get("country", ""),
                        "latitude": float(item.get("lat")),
                        "longitude": float(item.get("lon"))
                    })
                self.cache.set("nominatim_search", cache_key, results)
                return results
        except Exception:
            pass

        return []
