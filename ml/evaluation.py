"""
Model Evaluation & Scientific Metrics.
"""

from typing import Dict, Any


def evaluate_forecast_skill(observed_temp: list, forecast_temp: list) -> Dict[str, float]:
    """Compute standard verification metrics (MAE, RMSE)."""
    if not observed_temp or not forecast_temp or len(observed_temp) != len(forecast_temp):
        return {"mae": 0.0, "rmse": 0.0}
    
    errors = [abs(o - f) for o, f in zip(observed_temp, forecast_temp)]
    sq_errors = [(o - f) ** 2 for o, f in zip(observed_temp, forecast_temp)]
    
    mae = sum(errors) / len(errors)
    rmse = (sum(sq_errors) / len(sq_errors)) ** 0.5
    
    return {
        "mae_c": round(mae, 2),
        "rmse_c": round(rmse, 2),
        "sample_size": len(observed_temp)
    }
