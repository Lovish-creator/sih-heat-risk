"""
Composite Thermal Hazard Quantification Engine.

Synthesizes UTCI, WBGT, and Heat Index into a normalized, scientifically grounded
Thermal Hazard Score on a continuous 0 to 100 scale.
"""

from typing import Dict, Any, Optional
from .utci import calculate_utci, classify_utci, calculate_vapor_pressure, calculate_mrt
from .wbgt import calculate_wbgt, classify_wbgt
from .heat_index import calculate_heat_index, classify_heat_index


def calculate_thermal_hazard(
    temp_c: float,
    relative_humidity_pct: float,
    wind_speed_10m_m_s: float = 1.0,
    solar_radiation_w_m2: float = 0.0,
    is_outdoor: bool = True
) -> Dict[str, Any]:
    """
    Compute comprehensive biometeorological hazard profile across UTCI, WBGT, and Heat Index.
    
    Args:
        temp_c: Dry-bulb air temperature in degrees Celsius.
        relative_humidity_pct: Relative humidity in percent.
        wind_speed_10m_m_s: Wind speed at 10m in m/s.
        solar_radiation_w_m2: Solar irradiance in W/m^2.
        is_outdoor: True for direct sunlight exposure.
        
    Returns:
        Dictionary containing all raw metrics, classifications, and composite hazard score (0-100).
    """
    # 1. Calculate UTCI (Broad outdoor human physiological stress)
    utci_val = calculate_utci(
        temp_c=temp_c,
        relative_humidity_pct=relative_humidity_pct,
        wind_speed_10m_m_s=wind_speed_10m_m_s,
        solar_radiation_w_m2=solar_radiation_w_m2
    )
    utci_info = classify_utci(utci_val)
    
    # 2. Calculate WBGT (Occupational outdoor labor capacity)
    wbgt_val = calculate_wbgt(
        temp_c=temp_c,
        relative_humidity_pct=relative_humidity_pct,
        wind_speed_10m_m_s=wind_speed_10m_m_s,
        solar_radiation_w_m2=solar_radiation_w_m2,
        is_outdoor=is_outdoor
    )
    wbgt_info = classify_wbgt(wbgt_val)
    
    # 3. Calculate NOAA Heat Index (Apparent temperature in shade)
    hi_val = calculate_heat_index(
        temp_c=temp_c,
        relative_humidity_pct=relative_humidity_pct
    )
    hi_info = classify_heat_index(hi_val)
    
    # 4. Derive intermediate physical variables for transparency
    vapor_pressure_hpa = calculate_vapor_pressure(temp_c, relative_humidity_pct)
    tmrt_c = calculate_mrt(temp_c, solar_radiation_w_m2, wind_speed_10m_m_s)
    
    # 5. Composite Normalized Thermal Hazard Score (0 - 100)
    # Weights: UTCI (0.60) + WBGT (0.25) + Heat Index (0.15)
    composite_hazard_score = (
        0.60 * utci_info["hazard_score"]
        + 0.25 * wbgt_info["hazard_score"]
        + 0.15 * hi_info["hazard_score"]
    )
    composite_hazard_score = max(0.0, min(100.0, round(composite_hazard_score, 1)))
    
    return {
        "inputs": {
            "temp_c": round(float(temp_c), 1),
            "relative_humidity_pct": round(float(relative_humidity_pct), 1),
            "wind_speed_10m_m_s": round(float(wind_speed_10m_m_s), 1),
            "solar_radiation_w_m2": round(float(solar_radiation_w_m2), 1),
            "is_outdoor": is_outdoor
        },
        "intermediates": {
            "vapor_pressure_hpa": round(vapor_pressure_hpa, 2),
            "mean_radiant_temp_c": round(tmrt_c, 1),
            "delta_tmrt_c": round(tmrt_c - temp_c, 1)
        },
        "metrics": {
            "utci": {
                "value_c": utci_val,
                "category": utci_info["category"],
                "color": utci_info["color"],
                "hazard_score": utci_info["hazard_score"],
                "description": utci_info["description"]
            },
            "wbgt": {
                "value_c": wbgt_val,
                "risk_level": wbgt_info["risk_level"],
                "color": wbgt_info["color"],
                "hazard_score": wbgt_info["hazard_score"],
                "work_rest_regimen": wbgt_info["work_rest_regimen"],
                "water_intake_l_hr": wbgt_info["min_water_intake_l_hr"],
                "description": wbgt_info["description"]
            },
            "heat_index": {
                "value_c": hi_val,
                "category": hi_info["category"],
                "color": hi_info["color"],
                "hazard_score": hi_info["hazard_score"],
                "description": hi_info["description"]
            }
        },
        "composite_hazard_score": composite_hazard_score
    }
