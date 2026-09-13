"""
SIH26083 Composite Human Heat-Health Risk Engine.

Combines physical biometeorological hazard, demographic vulnerability,
and cumulative heatwave duration into an interpretable Relative Heat-Health Risk Score (0-100).

SCIENTIFIC & ETHICAL DISCLAIMER:
This index represents a relative heat-health prioritisation and early warning score
for municipal disaster mitigation. It is NOT a clinical diagnosis or mortality prediction.
"""

import os
import yaml
from typing import Dict, Any, Optional
from ..core.constants import DURATION_SCALING, AlertLevel


class HeatRiskEngine:
    """
    Evaluates human heat-health risk across spatial units (wards/zones)
    and forecast temporal horizons (D+1 to D+5).
    """

    def __init__(self, config_path: Optional[str] = "config/risk_weights.yaml"):
        self.model_version = "baseline-0.2"
        self.weights = {
            "thermal_hazard": 0.55,
            "demographic_vulnerability": 0.30,
            "heatwave_duration": 0.15
        }
        self.duration_scaling = DURATION_SCALING
        self._load_config(config_path)
        self._validate_weights()

    def _load_config(self, config_path: Optional[str]):
        """Load weights from YAML configuration if present."""
        if config_path:
            candidates = [
                config_path,
                os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", config_path)),
                os.path.abspath(os.path.join(os.getcwd(), config_path))
            ]
            for p in candidates:
                if p and os.path.exists(p):
                    try:
                        with open(p, "r", encoding="utf-8") as f:
                            cfg = yaml.safe_load(f)
                            if cfg and "weights" in cfg:
                                self.weights["thermal_hazard"] = float(cfg["weights"]["thermal_hazard"].get("weight", 0.55))
                                self.weights["demographic_vulnerability"] = float(cfg["weights"]["demographic_vulnerability"].get("weight", 0.30))
                                self.weights["heatwave_duration"] = float(cfg["weights"]["heatwave_duration"].get("weight", 0.15))
                                if "model_version" in cfg:
                                    self.model_version = cfg["model_version"]
                                break
                    except Exception:
                        pass

    def _validate_weights(self):
        """Validate that multi-criteria weights sum to 1.0 within floating point tolerance."""
        total_w = sum(self.weights.values())
        if abs(total_w - 1.0) > 1e-5:
            raise ValueError(f"Risk model weights must sum to 1.0 (current sum: {total_w:.6f}).")

    def calculate_risk(
        self,
        hazard_score: float,
        vulnerability_score: float,
        consecutive_heat_days: int = 1
    ) -> Dict[str, Any]:
        """
        Calculate composite Relative Heat-Health Risk Score for a given hazard, vulnerability, and duration.
        
        Args:
            hazard_score: Normalized thermal hazard score (0 - 100).
            vulnerability_score: Normalized demographic vulnerability score (0 - 100).
            consecutive_heat_days: Consecutive days exceeding strong thermal stress (1 to 5+).
            
        Returns:
            Dictionary containing final risk score, alert level, color code, and component sub-scores.
        """
        hz = max(0.0, min(100.0, float(hazard_score)))
        vl = max(0.0, min(100.0, float(vulnerability_score)))
        
        # Duration multiplier (0.0 to 1.0)
        days = max(1, int(consecutive_heat_days))
        dur_factor = self.duration_scaling.get(days, 1.0)
        dur_score = dur_factor * 100.0

        # Weighted component contributions
        w_hz = self.weights["thermal_hazard"]
        w_vl = self.weights["demographic_vulnerability"]
        w_dr = self.weights["heatwave_duration"]

        c_hazard = round(w_hz * hz, 2)
        c_vuln = round(w_vl * vl, 2)
        c_dur = round(w_dr * dur_score, 2)

        raw_risk = c_hazard + c_vuln + c_dur
        risk_score = max(0.0, min(100.0, round(raw_risk, 1)))

        # 4-Tier Alert Classification (IMD / NDMA Aligned)
        if risk_score > 75.0:
            alert = {
                "level": AlertLevel.RED.value,
                "label": "Warning (Severe Heat-Health Risk)",
                "color": "#dc3545",
                "action_summary": "Emergency heat action protocols active; halt heavy outdoor work 11:00-16:00."
            }
        elif 50.0 < risk_score <= 75.0:
            alert = {
                "level": AlertLevel.ORANGE.value,
                "label": "Alert (High Heat-Health Risk)",
                "color": "#fd7e14",
                "action_summary": "Be prepared; mandatory shaded rest cycles for workers and active cooling shelters."
            }
        elif 25.0 < risk_score <= 50.0:
            alert = {
                "level": AlertLevel.YELLOW.value,
                "label": "Watch (Moderate Heat-Health Risk)",
                "color": "#ffc107",
                "action_summary": "Stay updated; ensure adequate hydration and monitoring of elderly & outdoor workers."
            }
        else:
            alert = {
                "level": AlertLevel.GREEN.value,
                "label": "Normal (Low Heat-Health Risk)",
                "color": "#198754",
                "action_summary": "Standard summer precautions; maintain normal outdoor activities."
            }

        return {
            "risk_score": risk_score,
            "alert_level": alert["level"],
            "alert_label": alert["label"],
            "alert_color": alert["color"],
            "action_summary": alert["action_summary"],
            "components": {
                "thermal_hazard": round(hz, 1),
                "demographic_vulnerability": round(vl, 1),
                "persistence": round(dur_score, 1),
                "weighted_contributions": {
                    "thermal_hazard": c_hazard,
                    "vulnerability": c_vuln,
                    "persistence": c_dur
                }
            },
            "weights": self.weights,
            "consecutive_heat_days": days,
            "risk_model": self.model_version,
            "disclaimer": "Relative heat-health prioritisation score ? not a clinical diagnosis or mortality forecast."
        }
