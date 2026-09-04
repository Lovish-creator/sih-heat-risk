"""
SIH26083 Composite Human Heat-Health Risk Engine.

Combines physical biometeorological hazard, demographic vulnerability,
and cumulative heatwave duration into an interpretable Relative Heat-Health Risk Score (0-100).
"""

import os
import yaml
from typing import Dict, Any, Optional, List


class HeatRiskEngine:
    """
    Evaluates human heat-health risk across spatial units (wards/zones)
    and forecast temporal horizons (D+1 to D+5).
    """

    def __init__(self, config_path: Optional[str] = None):
        self.weights = {
            "thermal_hazard": 0.55,
            "demographic_vulnerability": 0.30,
            "heatwave_duration": 0.15
        }
        self.duration_scaling = {
            1: 0.0,
            2: 0.33,
            3: 0.66,
            4: 1.0,
            5: 1.0
        }
        self._load_config(config_path)

    def _load_config(self, config_path: Optional[str]):
        """Load weights from YAML configuration if present."""
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = yaml.safe_load(f)
                    if cfg and "weights" in cfg:
                        self.weights["thermal_hazard"] = cfg["weights"]["thermal_hazard"].get("weight", 0.55)
                        self.weights["demographic_vulnerability"] = cfg["weights"]["demographic_vulnerability"].get("weight", 0.30)
                        self.weights["heatwave_duration"] = cfg["weights"]["heatwave_duration"].get("weight", 0.15)
            except Exception as e:
                # Fallback to standard weights
                pass

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
            Dictionary containing final risk score, alert level, color code, and sub-score breakdown.
        """
        hz = max(0.0, min(100.0, float(hazard_score)))
        vl = max(0.0, min(100.0, float(vulnerability_score)))
        
        # Duration multiplier (0.0 to 1.0)
        days = max(1, int(consecutive_heat_days))
        dur_factor = self.duration_scaling.get(days, 1.0)
        dur_score = dur_factor * 100.0

        # Linear multi-criteria composition
        w_hz = self.weights["thermal_hazard"]
        w_vl = self.weights["demographic_vulnerability"]
        w_dr = self.weights["heatwave_duration"]

        raw_risk = (w_hz * hz) + (w_vl * vl) + (w_dr * dur_score)
        risk_score = max(0.0, min(100.0, round(raw_risk, 1)))

        # 4-Tier Alert Classification (IMD-Aligned)
        if risk_score > 75.0:
            alert = {
                "level": "RED",
                "label": "Warning (Severe Heat-Health Risk)",
                "color": "#dc3545",
                "action_summary": "Emergency heat action protocols active; halt heavy outdoor work 11:00-16:00."
            }
        elif 50.0 < risk_score <= 75.0:
            alert = {
                "level": "ORANGE",
                "label": "Alert (High Heat-Health Risk)",
                "color": "#fd7e14",
                "action_summary": "Be prepared; mandatory shaded rest cycles for workers and active cooling shelters."
            }
        elif 25.0 < risk_score <= 50.0:
            alert = {
                "level": "YELLOW",
                "label": "Watch (Moderate Heat-Health Risk)",
                "color": "#ffc107",
                "action_summary": "Be updated; avoid prolonged direct sun; ensure continuous hydration."
            }
        else:
            alert = {
                "level": "GREEN",
                "label": "Normal (Low Heat-Health Risk)",
                "color": "#28a745",
                "action_summary": "Standard summer precautions; normal activities permissible."
            }

        return {
            "risk_score": risk_score,
            "alert_level": alert["level"],
            "alert_label": alert["label"],
            "alert_color": alert["color"],
            "action_summary": alert["action_summary"],
            "breakdown": {
                "hazard_contribution": round(w_hz * hz, 1),
                "vulnerability_contribution": round(w_vl * vl, 1),
                "duration_contribution": round(w_dr * dur_score, 1),
                "weights_used": self.weights,
                "consecutive_days": days
            },
            "disclaimer": "Prototype Relative Heat-Health Risk Estimate — not a clinical diagnosis or absolute mortality forecast."
        }
