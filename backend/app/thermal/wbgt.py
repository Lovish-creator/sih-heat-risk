"""
Wet Bulb Globe Temperature (WBGT) Occupational Heat Stress Engine.

Implements standard outdoor and indoor/shade WBGT formulations per ISO 7243 and NIOSH 2016,
using Stull's empirical psychrometric wet-bulb formulation and Liljegren's black globe estimation.
"""

import math
from typing import Dict, Any, Optional


def calculate_wet_bulb_stull(temp_c: float, relative_humidity_pct: float) -> float:
    """
    Calculate psychrometric wet-bulb temperature (Tw) in degrees Celsius
    using the highly accurate empirical formula by Roland Stull (2011).
    
    Valid for -20 C <= Ta <= 50 C and 5% <= RH <= 99%.
    
    Args:
        temp_c: Dry-bulb air temperature in degrees Celsius.
        relative_humidity_pct: Relative humidity in percent.
        
    Returns:
        Wet-bulb temperature in degrees Celsius.
    """
    ta = float(temp_c)
    rh = max(1.0, min(100.0, float(relative_humidity_pct)))
    
    # Stull (2011) equation
    tw = (
        ta * math.atan(0.151977 * math.sqrt(rh + 8.313659))
        + math.atan(ta + rh)
        - math.atan(rh - 1.676331)
        + 0.00391838 * (rh ** 1.5) * math.atan(0.023101 * rh)
        - 4.686035
    )
    return tw


def calculate_globe_temp(
    temp_c: float,
    solar_radiation_w_m2: float,
    wind_speed_2m_m_s: float = 1.0
) -> float:
    """
    Estimate standard 150mm matte-black globe temperature (Tg) in degrees Celsius
    from air temperature, solar irradiance, and surface wind speed (Liljegren et al. / Bernard).
    
    Args:
        temp_c: Dry-bulb air temperature in degrees Celsius.
        solar_radiation_w_m2: All-sky solar irradiance in W/m^2.
        wind_speed_2m_m_s: Wind speed at 2 meters height in m/s.
        
    Returns:
        Black globe temperature in degrees Celsius.
    """
    ta = float(temp_c)
    s = max(0.0, float(solar_radiation_w_m2))
    v = max(0.2, float(wind_speed_2m_m_s))
    
    # Radiative equilibrium temperature bump
    tg_offset = (0.0149 * s) / (v**0.6 + 0.05)
    return ta + tg_offset


def calculate_wbgt(
    temp_c: float,
    relative_humidity_pct: float,
    wind_speed_10m_m_s: float = 1.0,
    solar_radiation_w_m2: float = 0.0,
    is_outdoor: bool = True
) -> float:
    """
    Calculate Wet Bulb Globe Temperature (WBGT) in degrees Celsius.
    
    Args:
        temp_c: Dry-bulb air temperature in degrees Celsius.
        relative_humidity_pct: Relative humidity in percent.
        wind_speed_10m_m_s: Wind speed at 10m height in m/s.
        solar_radiation_w_m2: Solar irradiance in W/m^2.
        is_outdoor: True for direct sunlight (0.7 Tnw + 0.2 Tg + 0.1 Ta),
                   False for indoor/shade (0.7 Tw + 0.3 Tg).
                   
    Returns:
        WBGT value in degrees Celsius.
    """
    ta = float(temp_c)
    rh = float(relative_humidity_pct)
    v10 = max(0.2, float(wind_speed_10m_m_s))
    
    # Scale wind from 10m to 2m height via 1/7th power law
    v2 = v10 * ((2.0 / 10.0) ** 0.2)
    
    # Psychrometric wet-bulb temperature
    tw = calculate_wet_bulb_stull(ta, rh)
    
    # Natural wet-bulb temperature (Tnw) with solar radiation adjustment
    if is_outdoor and solar_radiation_w_m2 > 0:
        tnw_offset = (0.0025 * solar_radiation_w_m2) / (v2**0.4 + 0.1)
        tnw = tw + min(2.5, tnw_offset)
    else:
        tnw = tw
        
    # Black globe temperature (Tg)
    tg = calculate_globe_temp(ta, solar_radiation_w_m2 if is_outdoor else 0.0, v2)
    
    if is_outdoor:
        wbgt = 0.7 * tnw + 0.2 * tg + 0.1 * ta
    else:
        wbgt = 0.7 * tw + 0.3 * tg
        
    return round(wbgt, 2)


def classify_wbgt(wbgt_val: float) -> Dict[str, Any]:
    """
    Classify a WBGT value according to NIOSH 2016 occupational heat exposure criteria.
    
    Args:
        wbgt_val: WBGT in degrees Celsius.
        
    Returns:
        Dictionary containing occupational risk category, prescribed rest regimen, and hydration guidelines.
    """
    w = float(wbgt_val)
    if w >= 32.0:
        return {
            "risk_level": "Extreme Risk",
            "code": "EXTREME_DANGER",
            "color": "#dc3545",
            "hazard_score": 100.0,
            "work_rest_regimen": "25% Work / 75% Rest per hour or Halt Heavy Outdoor Labor",
            "min_water_intake_l_hr": 1.0,
            "description": "High physiological heat strain; severe heat stroke hazard for outdoor workers."
        }
    elif 30.0 <= w < 32.0:
        return {
            "risk_level": "High Risk",
            "code": "HIGH_RISK",
            "color": "#fd7e14",
            "hazard_score": 75.0,
            "work_rest_regimen": "50% Work / 50% Rest per hour under designated shaded cooling zones",
            "min_water_intake_l_hr": 1.0,
            "description": "Substantial heat strain; frequent mandatory cooling intervals required."
        }
    elif 28.0 <= w < 30.0:
        return {
            "risk_level": "Moderate Risk",
            "code": "MODERATE_RISK",
            "color": "#ffc107",
            "hazard_score": 45.0,
            "work_rest_regimen": "75% Work / 25% Rest per hour under shade",
            "min_water_intake_l_hr": 0.75,
            "description": "Moderate heat strain; monitor workers for early fatigue and dehydration."
        }
    else:
        return {
            "risk_level": "Low Risk",
            "code": "LOW_RISK",
            "color": "#28a745",
            "hazard_score": 15.0,
            "work_rest_regimen": "Continuous work permissible (routine 10-15 min break every 2 hours)",
            "min_water_intake_l_hr": 0.5,
            "description": "Low occupational heat strain under standard labor conditions."
        }
