"""
Model Registry & Version Management.
Tracks active model version, parameters, and metadata.
"""

from typing import Dict, Any, Optional


class ModelRegistry:
    """
    Registry maintaining active and experimental heat-health risk models.
    """

    def __init__(self):
        self._models = {
            "deterministic_baseline": {
                "version": "baseline-0.2",
                "type": "Deterministic Biometeorological Multi-Criteria Index",
                "is_active": True,
                "description": "UTCI (0.55) + Census PCA Vulnerability (0.30) + Consecutive Duration (0.15)",
                "status": "PRODUCTION_DEFAULT"
            },
            "dlnm_epidemiological": {
                "version": "dlnm-0.1-alpha",
                "type": "Distributed Lag Non-Linear Model",
                "is_active": False,
                "description": "Statistical regression requiring verified district health registry data",
                "status": "RESEARCH_STUB"
            }
        }

    def get_active_model_info(self) -> Dict[str, Any]:
        for k, v in self._models.items():
            if v.get("is_active"):
                return {"model_id": k, **v}
        return {"model_id": "deterministic_baseline", **self._models["deterministic_baseline"]}

    def list_all_models(self) -> Dict[str, Any]:
        return self._models
