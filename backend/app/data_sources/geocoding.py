"""
OpenStreetMap Nominatim Geocoding & Reverse Geocoding Adapter.

Resolves geographic coordinates (lat/lon) into human-readable address hierarchies
(ward, suburb, city, district, state, country) and allows searching any global location.
Zero API keys required (Open Data / OpenStreetMap).
"""

import requests
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

    def search_locations(self, query: str, limit: int = 8) -> List[Dict[str, Any]]:
        """
        Search for locations / cities by name combining Pan-India Census database and Nominatim.
        """
        q_clean = query.strip()
        if not q_clean:
            return []

        cache_key = {"q": q_clean.lower(), "limit": limit, "type": "search"}
        cached = self.cache.get("nominatim_search", cache_key)
        if cached:
            return cached

        results: List[Dict[str, Any]] = []
        seen_names = set()

        # 1. Fast Local Pan-India Registry, Ward Profiles & District Search
        try:
            from ..gis.city_data import MUNICIPAL_WARD_PROFILES
            from ..gis.india_cities import INDIA_CITIES_REGISTRY
            from ..vulnerability.demographic import DemographicVulnerabilityEngine
            ql = q_clean.lower()

            # A. Match Municipal Ward Profiles
            for cid, prof in MUNICIPAL_WARD_PROFILES.items():
                cname = prof.get("city_name", "")
                sname = prof.get("state_name", "")
                if ql in cid or ql in cname.lower() or cname.lower().startswith(ql):
                    key = f"{cname}, {sname}".lower()
                    if key not in seen_names:
                        seen_names.add(key)
                        results.append({
                            "name": f"{cname}, {sname}, India",
                            "city": cname,
                            "state": sname,
                            "country": "India",
                            "latitude": float(prof["center"]["lat"]),
                            "longitude": float(prof["center"]["lon"])
                        })

            # B. Match Comprehensive Pan-India Cities Registry
            for item in INDIA_CITIES_REGISTRY:
                cname = item.get("city", "")
                sname = item.get("state", "")
                if ql in cname.lower() or cname.lower().startswith(ql):
                    key = f"{cname}, {sname}".lower()
                    if key not in seen_names:
                        seen_names.add(key)
                        results.append({
                            "name": f"{cname}, {sname}, India",
                            "city": cname,
                            "state": sname,
                            "country": "India",
                            "latitude": float(item["lat"]),
                            "longitude": float(item["lon"])
                        })

            # C. Check Census districts
            vuln = DemographicVulnerabilityEngine()
            districts = vuln._load_districts()
            for d in districts:
                dname = d.get("district_name", "")
                sname = d.get("state_name", "")
                lat = d.get("latitude")
                lon = d.get("longitude")
                if (ql in dname.lower() or dname.lower().startswith(ql)) and lat is not None and lon is not None:
                    key = f"{dname}, {sname}".lower()
                    if key not in seen_names:
                        seen_names.add(key)
                        results.append({
                            "name": f"{dname} District, {sname}, India",
                            "city": dname,
                            "state": sname,
                            "country": "India",
                            "latitude": float(lat),
                            "longitude": float(lon)
                        })
        except Exception:
            pass

        # If we have sufficient local verified matches, return immediately (sub-millisecond latency)
        if len(results) >= limit:
            final_res = results[:limit]
            self.cache.set("nominatim_search", cache_key, final_res)
            return final_res

        # 2. OpenStreetMap Nominatim Live Search for exact towns/suburbs
        headers = {"User-Agent": self.USER_AGENT}
        params = {
            "q": f"{q_clean}, India" if ("india" not in q_clean.lower()) else q_clean,
            "format": "json",
            "addressdetails": 1,
            "limit": limit
        }

        try:
            res = requests.get(self.SEARCH_URL, params=params, headers=headers, timeout=min(self.timeout, 3))
            if res.status_code == 200:
                items = res.json()
                for item in items:
                    addr = item.get("address", {})
                    city = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("municipality") or addr.get("county") or item.get("name", "Unknown")
                    dname = item.get("display_name", "")
                    lat = float(item.get("lat"))
                    lon = float(item.get("lon"))
                    
                    key = f"{city}_{round(lat, 2)}_{round(lon, 2)}".lower()
                    if key not in seen_names and city.lower() not in seen_names:
                        seen_names.add(key)
                        seen_names.add(city.lower())
                        results.append({
                            "name": dname,
                            "city": city,
                            "state": addr.get("state", ""),
                            "country": addr.get("country", "India"),
                            "latitude": lat,
                            "longitude": lon
                        })
                    if key not in seen_names and len(results) < limit:
                        seen_names.add(key)
                        results.append({
                            "name": dname,
                            "city": city,
                            "state": addr.get("state", ""),
                            "country": addr.get("country", "India"),
                            "latitude": lat,
                            "longitude": lon
                        })
        except Exception:
            pass

        final_results = results[:limit]
        if final_results:
            self.cache.set("nominatim_search", cache_key, final_results)
        return final_results

    def get_ip_location(self, client_ip: Optional[str] = None) -> Dict[str, Any]:
        """
        Detect geolocation from client IP address with multi-provider fallbacks.
        """
        cache_key = {"ip": client_ip or "self", "type": "ip_geolocate"}
        cached = self.cache.get("ip_geolocate", cache_key)
        if cached:
            return cached

        providers = [
            ("https://ipwho.is/" + (f"{client_ip}" if client_ip else ""),
             lambda d: (float(d["latitude"]), float(d["longitude"]), d.get("city", "Detected City"), d.get("region", ""), d.get("country", "India"))),
            ("http://ip-api.com/json/" + (f"{client_ip}" if client_ip else ""),
             lambda d: (float(d["lat"]), float(d["lon"]), d.get("city", "Detected City"), d.get("regionName", ""), d.get("country", "India"))),
            ("https://ipapi.co/" + (f"{client_ip}/" if client_ip else "") + "json/",
             lambda d: (float(d["latitude"]), float(d["longitude"]), d.get("city", "Detected City"), d.get("region", ""), d.get("country", "India"))),
        ]

        for url, parser in providers:
            try:
                res = requests.get(url, timeout=self.timeout)
                if res.status_code == 200:
                    data = res.json()
                    if data.get("success", True) is not False:
                        lat, lon, city, region, country = parser(data)
                        result = {
                            "status": "success",
                            "latitude": lat,
                            "longitude": lon,
                            "city": city,
                            "region": region,
                            "country": country,
                            "display_name": f"{city}, {region}, {country}" if region else f"{city}, {country}",
                            "source": url
                        }
                        self.cache.set("ip_geolocate", cache_key, result)
                        return result
            except Exception:
                continue

        # Ultimate fallback
        return {
            "status": "fallback",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "city": "New Delhi",
            "region": "Delhi",
            "country": "India",
            "display_name": "New Delhi, Delhi, India",
            "source": "Default Baseline"
        }

