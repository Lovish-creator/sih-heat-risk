"""
SIH26083 Biometeorological & Thermal Stress Calculation Engines.
Includes validated implementations of:
- UTCI (Universal Thermal Climate Index)
- WBGT (Wet Bulb Globe Temperature - NIOSH / ISO 7243)
- Heat Index (NOAA / NWS Rothfusz Formulation)
- Thermal Hazard Normalizer
"""

from .utci import calculate_utci, classify_utci, calculate_vapor_pressure, calculate_mrt
from .wbgt import calculate_wbgt, classify_wbgt, calculate_wet_bulb_stull, calculate_globe_temp
from .heat_index import calculate_heat_index, classify_heat_index
from .hazard import calculate_thermal_hazard

__all__ = [
    "calculate_utci",
    "classify_utci",
    "calculate_vapor_pressure",
    "calculate_mrt",
    "calculate_wbgt",
    "classify_wbgt",
    "calculate_wet_bulb_stull",
    "calculate_globe_temp",
    "calculate_heat_index",
    "classify_heat_index",
    "calculate_thermal_hazard",
]
