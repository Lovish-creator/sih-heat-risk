"""
Biometeorological Feature Engineering for Epidemiological Analysis.
Computes multi-day lag features, nocturnal cooling metrics, and thermal stress thresholds.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np


class BiometeorologicalFeatureExtractor:
    """
    Constructs distributed lag variables and compound exposure indicators.
    """

    @staticmethod
    def extract_lag_features(df: pd.DataFrame, max_lag_days: int = 7) -> pd.DataFrame:
        """
        Generate multi-day lag variables for cumulative thermal exposure.
        """
        out = df.copy()
        for lag in range(1, max_lag_days + 1):
            if "utci_c" in out.columns:
                out[f"utci_lag_{lag}"] = out["utci_c"].shift(lag)
            if "temp_c" in out.columns:
                out[f"temp_lag_{lag}"] = out["temp_c"].shift(lag)
        return out

    @staticmethod
    def extract_compound_stress_indices(temp_c: float, rh_pct: float, wind_speed: float, solar_rad: float) -> Dict[str, float]:
        """
        Extract normalized feature vector for inference pipeline.
        """
        return {
            "temp_c": float(temp_c),
            "rh_pct": float(rh_pct),
            "wind_speed": float(wind_speed),
            "solar_rad": float(solar_rad),
            "vapor_pressure_proxy": float((rh_pct / 100.0) * (temp_c ** 1.8)),
            "apparent_heat_flux": float(solar_rad / max(0.5, wind_speed))
        }
