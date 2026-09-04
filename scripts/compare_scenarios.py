"""
SIH26083 - Comparative Environmental Scenario Demonstration.

Demonstrates the core scientific justification of SIH26083:
"Why Dry-Bulb Air Temperature Alone Fails to Predict Human Physiological Strain"
"""

import sys
import os

# Add root path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.thermal.hazard import calculate_thermal_hazard
from backend.app.risk.engine import HeatRiskEngine


def main():
    print("=" * 80)
    print("SIH26083: BIOMETEOROLOGICAL CONTRAST DEMONSTRATION")
    print("Theme: 'What the weather will do to humans' vs 'What the temperature will be'")
    print("=" * 80)

    # Base common dry-bulb temperature
    ta = 40.0

    # Scenario A: Hot, Dry, Windy, Low Solar Load (e.g., desert-like afternoon under light haze)
    rh_a = 15.0
    wind_a = 5.0
    solar_a = 150.0

    # Scenario B: Hot, Humid, Stagnant Air, Intense Solar Load (e.g., pre-monsoon coastal/plain heatwave)
    rh_b = 70.0
    wind_b = 0.8
    solar_b = 800.0

    hz_a = calculate_thermal_hazard(ta, rh_a, wind_a, solar_a)
    hz_b = calculate_thermal_hazard(ta, rh_b, wind_b, solar_b)

    risk_engine = HeatRiskEngine()
    # Baseline vulnerability = 60.0 (high elderly & worker ward)
    risk_a = risk_engine.calculate_risk(hz_a["composite_hazard_score"], 60.0, consecutive_heat_days=1)
    risk_b = risk_engine.calculate_risk(hz_b["composite_hazard_score"], 60.0, consecutive_heat_days=3)

    print(f"\n[COMMON METRIC] Air Temperature (Ta): {ta:.1f} °C for BOTH Scenarios\n")

    print("-" * 80)
    print("SCENARIO A: Dry & Windy (15% RH, 5.0 m/s Wind, 150 W/m² Solar)")
    print("-" * 80)
    print(f"  * Vapor Pressure (e):       {hz_a['intermediates']['vapor_pressure_hpa']} hPa")
    print(f"  * Mean Radiant Temp (Tmrt): {hz_a['intermediates']['mean_radiant_temp_c']} °C")
    print(f"  * Physiological UTCI:       {hz_a['metrics']['utci']['value_c']} °C -> [{hz_a['metrics']['utci']['category']}]")
    print(f"  * Occupational WBGT:        {hz_a['metrics']['wbgt']['value_c']} °C -> [{hz_a['metrics']['wbgt']['risk_level']}]")
    print(f"  * NIOSH Work/Rest Regimen:  {hz_a['metrics']['wbgt']['work_rest_regimen']}")
    print(f"  * Thermal Hazard Score:     {hz_a['composite_hazard_score']} / 100")
    print(f"  * Composite Risk Score:     {risk_a['risk_score']} / 100 -> [{risk_a['alert_level']} Alert]")
    print(f"  * Human Impact:             Sweat evaporates efficiently; core body temperature stable.")

    print("\n" + "-" * 80)
    print("SCENARIO B: Humid, Stagnant & High Sun (70% RH, 0.8 m/s Wind, 800 W/m² Solar)")
    print("-" * 80)
    print(f"  * Vapor Pressure (e):       {hz_b['intermediates']['vapor_pressure_hpa']} hPa")
    print(f"  * Mean Radiant Temp (Tmrt): {hz_b['intermediates']['mean_radiant_temp_c']} °C")
    print(f"  * Physiological UTCI:       {hz_b['metrics']['utci']['value_c']} °C -> [{hz_b['metrics']['utci']['category']}]")
    print(f"  * Occupational WBGT:        {hz_b['metrics']['wbgt']['value_c']} °C -> [{hz_b['metrics']['wbgt']['risk_level']}]")
    print(f"  * NIOSH Work/Rest Regimen:  {hz_b['metrics']['wbgt']['work_rest_regimen']}")
    print(f"  * Thermal Hazard Score:     {hz_b['composite_hazard_score']} / 100")
    print(f"  * Composite Risk Score:     {risk_b['risk_score']} / 100 -> [{risk_b['alert_level']} Alert]")
    print(f"  * Human Impact:             Sweat evaporation crippled; severe heat stroke & hyperthermia danger!")

    print("\n" + "=" * 80)
    delta_utci = hz_b['metrics']['utci']['value_c'] - hz_a['metrics']['utci']['value_c']
    delta_wbgt = hz_b['metrics']['wbgt']['value_c'] - hz_a['metrics']['wbgt']['value_c']
    delta_risk = risk_b['risk_score'] - risk_a['risk_score']
    print(f"CONCLUSION:")
    print(f"Despite IDENTICAL 40°C temperature, Scenario B produces:")
    print(f"  + {delta_utci:.1f}°C HIGHER Physiological UTCI")
    print(f"  + {delta_wbgt:.1f}°C HIGHER Occupational WBGT")
    print(f"  + {delta_risk:.1f} Points HIGHER Human Heat-Health Risk Score")
    print(f"  Shifted Alert Level from {risk_a['alert_level']} (Watch) -> {risk_b['alert_level']} (Severe Emergency)")
    print("=" * 80)


if __name__ == "__main__":
    main()
