"""
NOAA / National Weather Service (NWS) Heat Index Engine.

Implements Lans P. Rothfusz's 9-term multiple regression formulation
with high and low relative humidity adjustments.
"""

import math
from typing import Dict, Any


def calculate_heat_index(temp_c: float, relative_humidity_pct: float) -> float:
    """
    Calculate NOAA/NWS Heat Index ("Feels Like" apparent temperature) in degrees Celsius.
    
    Args:
        temp_c: Dry-bulb air temperature in degrees Celsius.
        relative_humidity_pct: Relative humidity in percent (0 to 100%).
        
    Returns:
        Heat Index in degrees Celsius.
    """
    tc = float(temp_c)
    rh = max(0.0, min(100.0, float(relative_humidity_pct)))
    
    # Convert Celsius to Fahrenheit
    tf = tc * 1.8 + 32.0
    
    # Below 80 F (26.7 C), use Steadman's simplified apparent temperature formula
    if tf < 80.0:
        hi_f = 0.5 * (tf + 61.0 + ((tf - 68.0) * 1.2) + (rh * 0.094))
        hi_c = (hi_f - 32.0) / 1.8
        return round(hi_c, 2)
        
    # Rothfusz 9-term polynomial
    hi_f = (
        -42.379
        + 2.04901523 * tf
        + 10.14333127 * rh
        - 0.22475541 * tf * rh
        - 0.00683783 * (tf ** 2)
        - 0.05481717 * (rh ** 2)
        + 0.00122874 * (tf ** 2) * rh
        + 0.00085282 * tf * (rh ** 2)
        - 0.00000199 * (tf ** 2) * (rh ** 2)
    )
    
    # Low humidity adjustment
    if rh < 13.0 and 80.0 <= tf <= 112.0:
        diff = abs(tf - 95.0)
        if diff <= 17.0:
            adj = -((13.0 - rh) / 4.0) * math.sqrt((17.0 - diff) / 17.0)
            hi_f += adj
            
    # High humidity adjustment
    elif rh > 85.0 and 80.0 <= tf <= 87.0:
        adj = ((rh - 85.0) / 10.0) * ((87.0 - tf) / 5.0)
        hi_f += adj
        
    # Convert back to Celsius
    hi_c = (hi_f - 32.0) / 1.8
    return round(hi_c, 2)


def classify_heat_index(hi_val_c: float) -> Dict[str, Any]:
    """
    Classify a Heat Index value into standard NOAA/NWS warning categories.
    
    Args:
        hi_val_c: Heat Index in degrees Celsius.
        
    Returns:
        Dictionary with category name, color, and normalized hazard score.
    """
    h = float(hi_val_c)
    if h >= 54.0:
        return {
            "category": "Extreme Danger",
            "code": "EXTREME_DANGER",
            "color": "#7f0000",
            "hazard_score": 100.0,
            "description": "Heat stroke imminent with continued physical exposure."
        }
    elif 41.0 <= h < 54.0:
        return {
            "category": "Danger",
            "code": "DANGER",
            "color": "#d73027",
            "hazard_score": 80.0,
            "description": "Heat cramps and heat exhaustion likely; heat stroke possible."
        }
    elif 32.0 <= h < 41.0:
        return {
            "category": "Extreme Caution",
            "code": "EXTREME_CAUTION",
            "color": "#f46d43",
            "hazard_score": 50.0,
            "description": "Heat cramps and physical fatigue possible with prolonged activity."
        }
    elif 27.0 <= h < 32.0:
        return {
            "category": "Caution",
            "code": "CAUTION",
            "color": "#fdae61",
            "hazard_score": 25.0,
            "description": "Fatigue possible with prolonged outdoor exposure."
        }
    else:
        return {
            "category": "Normal",
            "code": "NORMAL",
            "color": "#1a9850",
            "hazard_score": 0.0,
            "description": "Minimal environmental heat hazard."
        }
