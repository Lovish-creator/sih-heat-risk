"""
Abstract Weather Provider Interface.
Defines the standard contract for meteorological and solar irradiance ingestion.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import date, datetime


class WeatherProvider(ABC):
    """
    Abstract base class for all meteorological data providers (NASA POWER, IMD, NCMRWF).
    """

    @abstractmethod
    def get_current_weather(self, lat: float, lon: float, city_id: str = "ahmedabad") -> Dict[str, Any]:
        """
        Fetch near-real-time current meteorological observations.
        
        Returns:
            Dictionary with keys: temp_c, relative_humidity_pct, wind_speed_10m_m_s,
                                solar_radiation_w_m2, timestamp, provider_name.
        """
        pass

    @abstractmethod
    def get_forecast_weather(
        self,
        lat: float,
        lon: float,
        city_id: str = "ahmedabad",
        days: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Fetch multi-day horizon meteorological forecast series (D+1 to D+5).
        
        Returns:
            List of daily dictionaries with forecast parameters and horizon index.
        """
        pass
