"""
CLI Script to fetch and cache meteorological data for a city profile.
"""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.data_sources.nasa_power import NASAPowerProvider
from backend.app.data_sources.cache import DataCache


def main():
    city = sys.argv[1] if len(sys.argv) > 1 else "ahmedabad"
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    cache = DataCache(cache_dir="data/cache")
    provider = NASAPowerProvider(cache=cache, demo_mode=True)
    
    # Coordinates for Ahmedabad
    lat, lon = 23.0225, 72.5714
    print(f"Fetching {days}-day meteorological forecast for {city.title()} ({lat}, {lon})...")
    
    forecast = provider.get_forecast_weather(lat, lon, city_id=city, days=days)
    print(json.dumps(forecast, indent=2))


if __name__ == "__main__":
    main()
