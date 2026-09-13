"""
ML Inference Pipeline.
Provides a unified interface with graceful fallback to deterministic biometeorological engine.
"""

from typing import Dict, Any
from backend.app.risk.engine import HeatRiskEngine
from backend.app.thermal.hazard import calculate_thermal_hazard


class RiskInferencePipeline:
    """
    Evaluates real-time risk scores using deterministic baseline or verified ML model.
    """

    def __init__(self):
        self.baseline_engine = HeatRiskEngine()

    def predict(
        self,
        temp_c: float,
        relative_humidity_pct: float,
        wind_speed_10m_m_s: float,
        solar_radiation_w_m2: float,
        vulnerability_score: float,
        consecutive_heat_days: int = 1
    ) -> Dict[str, Any]:
        # Calculate physical hazard
        hz = calculate_thermal_hazard(
            temp_c=temp_c,
            relative_humidity_pct=relative_humidity_pct,
            wind_speed_10m_m_s=wind_speed_10m_m_s,
            solar_radiation_w_m2=solar_radiation_w_m2
        )

        # Evaluate risk using active deterministic baseline
        risk_result = self.baseline_engine.calculate_risk(
            hazard_score=hz["composite_hazard_score"],
            vulnerability_score=vulnerability_score,
            consecutive_heat_days=consecutive_heat_days
        )

        return {
            "hazard_analysis": hz,
            "risk_assessment": risk_result,
            "inference_mode": "DETERMINISTIC_BASELINE"
        }
