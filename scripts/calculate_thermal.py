"""
CLI Script to calculate biometeorological indices from input arguments.
Usage: python scripts/calculate_thermal.py <temp_c> <rh_pct> <wind_m_s> <solar_w_m2>
"""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.thermal.hazard import calculate_thermal_hazard


def main():
    if len(sys.argv) < 5:
        print("Usage: python scripts/calculate_thermal.py <temp_c> <rh_pct> <wind_10m_m_s> <solar_w_m2>")
        sys.exit(1)

    t = float(sys.argv[1])
    rh = float(sys.argv[2])
    ws = float(sys.argv[3])
    solar = float(sys.argv[4])

    res = calculate_thermal_hazard(temp_c=t, relative_humidity_pct=rh, wind_speed_10m_m_s=ws, solar_radiation_w_m2=solar)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
