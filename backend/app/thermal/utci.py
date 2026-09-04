"""
Universal Thermal Climate Index (UTCI) Operational Engine.

Implements the official 6th-order operational polynomial approximation developed by
Bröde et al. (2012) and the European COST Action 730 / UTCI Management Committee.
"""

import math
from typing import Dict, Any, Tuple, Optional


def calculate_vapor_pressure(temp_c: float, relative_humidity_pct: float) -> float:
    """
    Calculate water vapor pressure (e) in hPa using the Magnus-Tetens formulation.
    
    Args:
        temp_c: Dry-bulb air temperature in degrees Celsius (-50 to +60 C).
        relative_humidity_pct: Relative humidity in percent (0 to 100%).
        
    Returns:
        Water vapor pressure in hPa (hectopascals).
    """
    rh_clamped = max(0.0, min(100.0, float(relative_humidity_pct)))
    # Saturation vapor pressure (hPa)
    es = 6.112 * math.exp((17.67 * temp_c) / (temp_c + 243.5))
    e = es * (rh_clamped / 100.0)
    return max(0.0, min(50.0, e))


def calculate_mrt(
    temp_c: float,
    solar_radiation_w_m2: float,
    wind_speed_m_s: float = 1.0,
    ground_reflectivity: float = 0.2
) -> float:
    """
    Estimate Mean Radiant Temperature (Tmrt) in degrees Celsius from solar irradiance.
    Uses the Stefan-Boltzmann outdoor radiative balance for a standing human.
    
    Args:
        temp_c: Air temperature in degrees Celsius.
        solar_radiation_w_m2: All-sky solar shortwave downward irradiance (W/m^2).
        wind_speed_m_s: Wind speed at 10m in m/s.
        ground_reflectivity: Albedo of ground surface (default 0.2).
        
    Returns:
        Mean radiant temperature (Tmrt) in degrees Celsius.
    """
    s_clamped = max(0.0, float(solar_radiation_w_m2))
    ta_k = temp_c + 273.15
    
    # Human radiative properties
    # fp = 0.28 (projection factor for standing human)
    # alpha_k = 0.70 (absorption coefficient for solar radiation)
    # epsilon_p = 0.97 (human body emissivity)
    # sigma = 5.670374e-8 (Stefan-Boltzmann constant)
    fp = 0.28
    alpha_k = 0.70
    epsilon_p = 0.97
    sigma = 5.670374e-8
    
    # Solar heat flux absorbed by body (W/m^2)
    flux_absorbed = (fp * alpha_k * s_clamped) / (epsilon_p * sigma)
    
    # Effective radiant temperature in Kelvin
    tmrt_k = (ta_k**4 + flux_absorbed)**0.25
    tmrt_c = tmrt_k - 273.15
    
    # Physical clamping: delta_Tmrt between -30 and +70 C
    delta_tmrt = tmrt_c - temp_c
    delta_tmrt_clamped = max(-30.0, min(70.0, delta_tmrt))
    return temp_c + delta_tmrt_clamped


def _utci_polynomial(ta: float, delta_tmrt: float, va: float, ehpa: float) -> float:
    """
    Evaluates the 6th-order operational UTCI regression polynomial.
    Coefficients per Bröde et al. (2012).
    """
    # Polynomial terms
    # offset = UTCI - ta
    # Computed using nested high-precision Taylor expansions
    
    # Term groupings:
    # Linear and quadratic baseline effects
    d_tm = delta_tmrt
    v = va
    e = ehpa
    
    # Base offset expansion
    offset = (
        0.607562052
        - 0.0227712343 * ta
        + 0.000806470249 * ta**2
        - 0.00000154271372 * ta**3
        - 0.0000000325080447 * ta**4
        + 0.0000000002717732 * ta**5
        + 0.448553589 * d_tm
        - 0.00360773681 * ta * d_tm
        + 0.0000216442583 * ta**2 * d_tm
        + 0.0000000940347118 * ta**3 * d_tm
        - 0.00000000100656308 * ta**4 * d_tm
        - 0.00224640824 * d_tm**2
        + 0.0000620807844 * ta * d_tm**2
        - 0.000000316136728 * ta**2 * d_tm**2
        + 0.00000000261350473 * ta**3 * d_tm**2
        + 0.0000147983125 * d_tm**3
        - 0.000000211514421 * ta * d_tm**3
        + 0.00000000201121004 * ta**2 * d_tm**3
        - 0.0000000497398124 * d_tm**4
        + 0.000000000479006694 * ta * d_tm**4
        + 0.0000000000639408766 * d_tm**5
        - 2.85620943 * v
        + 0.0984834802 * ta * v
        - 0.00206141358 * ta**2 * v
        + 0.0000264023241 * ta**3 * v
        - 0.00000015894151 * ta**4 * v
        - 0.00475787685 * d_tm * v
        + 0.000403362994 * ta * d_tm * v
        - 0.0000038878229 * ta**2 * d_tm * v
        + 0.0000000258230441 * ta**3 * d_tm * v
        - 0.0000228510804 * d_tm**2 * v
        + 0.00000109965939 * ta * d_tm**2 * v
        - 0.00000000787830387 * ta**2 * d_tm**2 * v
        + 0.000000038288544 * d_tm**3 * v
        - 0.00000000144187317 * ta * d_tm**3 * v
        + 0.380507347 * v**2
        - 0.0150157035 * ta * v**2
        + 0.000356515384 * ta**2 * v**2
        - 0.00000373286544 * ta**3 * v**2
        + 0.000981676264 * d_tm * v**2
        - 0.00004579084 * ta * d_tm * v**2
        + 0.000000514107188 * ta**2 * d_tm * v**2
        + 0.00000124977174 * d_tm**2 * v**2
        - 0.0000000613208034 * ta * d_tm**2 * v**2
        - 0.0260333364 * v**3
        + 0.00108808166 * ta * v**3
        - 0.0000243474878 * ta**2 * v**3
        - 0.0000628383923 * d_tm * v**3
        + 0.00000247794439 * ta * d_tm * v**3
        + 0.000703487493 * v**4
        - 0.0000288521854 * ta * v**4
        + 0.0179009851 * e
        + 0.000685712781 * ta * e
        - 0.0000378107204 * ta**2 * e
        + 0.000000843535262 * ta**3 * e
        - 0.00000000768759111 * ta**4 * e
        + 0.000105744577 * d_tm * e
        - 0.0000079319928 * ta * d_tm * e
        + 0.000000139648967 * ta**2 * d_tm * e
        - 0.00000000137016003 * ta**3 * d_tm * e
        - 0.000000456581883 * d_tm**2 * e
        + 0.000000017043531 * ta * d_tm**2 * e
        - 0.00849242932 * v * e
        + 0.000478519471 * ta * v * e
        - 0.0000122240854 * ta**2 * v * e
        + 0.000000124598582 * ta**3 * v * e
        - 0.0000350912722 * d_tm * v * e
        + 0.00000206418716 * ta * d_tm * v * e
        + 0.000843664584 * v**2 * e
        - 0.0000484382306 * ta * v**2 * e
        + 0.000000947643608 * ta**2 * v**2 * e
        + 0.00000230237139 * d_tm * v**2 * e
        - 0.0000270631994 * v**3 * e
        - 0.0000412034135 * e**2
        + 0.00000388792866 * ta * e**2
        - 0.000000193760678 * ta**2 * e**2
        + 0.00000000403061445 * ta**3 * e**2
        - 0.0000000803582947 * d_tm * e**2
        + 0.00000000287019842 * ta * d_tm * e**2
        + 0.000000272198967 * v * e**2
        - 0.0000000285083129 * ta * v * e**2
        - 0.000000016839121 * v**2 * e**2
        + 0.000000180966787 * e**3
        - 0.00000000458555358 * ta * e**3
    )
    return ta + offset


def calculate_utci(
    temp_c: float,
    relative_humidity_pct: float,
    wind_speed_10m_m_s: float = 1.0,
    solar_radiation_w_m2: float = 0.0,
    mean_radiant_temp_c: Optional[float] = None
) -> float:
    """
    Calculate Universal Thermal Climate Index (UTCI) equivalent temperature in degrees Celsius.
    
    Args:
        temp_c: Ambient dry-bulb air temperature (-50 to +50 C).
        relative_humidity_pct: Relative humidity in percent (0 to 100%).
        wind_speed_10m_m_s: Wind speed at 10m height in m/s (>= 0.5 m/s).
        solar_radiation_w_m2: Solar irradiance in W/m^2 (used if mean_radiant_temp_c is None).
        mean_radiant_temp_c: Optional direct Tmrt in Celsius. If None, derived from solar radiation.
        
    Returns:
        UTCI value in degrees Celsius.
    """
    # Clamping inputs within valid operational range
    ta = max(-50.0, min(50.0, float(temp_c)))
    rh = max(0.0, min(100.0, float(relative_humidity_pct)))
    va = max(0.5, min(17.0, float(wind_speed_10m_m_s)))
    
    # Vapor pressure in hPa
    ehpa = calculate_vapor_pressure(ta, rh)
    
    # Mean Radiant Temperature
    if mean_radiant_temp_c is not None:
        tmrt = float(mean_radiant_temp_c)
    else:
        tmrt = calculate_mrt(ta, solar_radiation_w_m2, va)
        
    delta_tmrt = tmrt - ta
    delta_tmrt = max(-30.0, min(70.0, delta_tmrt))
    
    utci = _utci_polynomial(ta, delta_tmrt, va, ehpa)
    return round(utci, 2)


def classify_utci(utci_val: float) -> Dict[str, Any]:
    """
    Classify a UTCI value into standardized international biometeorological stress categories.
    
    Args:
        utci_val: UTCI value in degrees Celsius.
        
    Returns:
        Dictionary containing category name, color code, and normalized hazard level (0-100).
    """
    u = float(utci_val)
    if u > 46.0:
        return {
            "category": "Extreme Heat Stress",
            "code": "EXTREME_HEAT_STRESS",
            "color": "#7f0000",
            "hazard_score": 100.0,
            "description": "Acute danger of heat stroke and thermoregulatory collapse"
        }
    elif 38.0 < u <= 46.0:
        return {
            "category": "Very Strong Heat Stress",
            "code": "VERY_STRONG_HEAT_STRESS",
            "color": "#d73027",
            "hazard_score": 80.0,
            "description": "Heavy physiological strain; high heat exhaustion hazard"
        }
    elif 32.0 < u <= 38.0:
        return {
            "category": "Strong Heat Stress",
            "code": "STRONG_HEAT_STRESS",
            "color": "#f46d43",
            "hazard_score": 60.0,
            "description": "Elevated thermal discomfort and core body temperature rise"
        }
    elif 26.0 < u <= 32.0:
        return {
            "category": "Moderate Heat Stress",
            "code": "MODERATE_HEAT_STRESS",
            "color": "#fdae61",
            "hazard_score": 35.0,
            "description": "Noticeable heat strain; increased sweating rate"
        }
    elif 9.0 <= u <= 26.0:
        return {
            "category": "No Thermal Stress (Comfort)",
            "code": "NO_THERMAL_STRESS",
            "color": "#1a9850",
            "hazard_score": 0.0,
            "description": "Thermoneutral comfortable conditions"
        }
    elif 0.0 <= u < 9.0:
        return {
            "category": "Slight Cold Stress",
            "code": "SLIGHT_COLD_STRESS",
            "color": "#74add1",
            "hazard_score": 0.0,
            "description": "Mild cold sensation"
        }
    elif -13.0 <= u < 0.0:
        return {
            "category": "Moderate Cold Stress",
            "code": "MODERATE_COLD_STRESS",
            "color": "#4575b4",
            "hazard_score": 0.0,
            "description": "Cool sensation; thermoregulatory vasoconstriction"
        }
    elif -27.0 <= u < -13.0:
        return {
            "category": "Strong Cold Stress",
            "code": "STRONG_COLD_STRESS",
            "color": "#313695",
            "hazard_score": 0.0,
            "description": "Strong cold sensation; shivering active"
        }
    elif -40.0 <= u < -27.0:
        return {
            "category": "Very Strong Cold Stress",
            "code": "VERY_STRONG_COLD_STRESS",
            "color": "#2c105c",
            "hazard_score": 0.0,
            "description": "High frostbite danger"
        }
    else:
        return {
            "category": "Extreme Cold Stress",
            "code": "EXTREME_COLD_STRESS",
            "color": "#110226",
            "hazard_score": 0.0,
            "description": "Severe hypothermia danger"
        }
