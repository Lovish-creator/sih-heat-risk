"""
ML Dataset Ingestion & Validation Pipelines.
Requires genuine verified health outcome records (e.g. IDSP / HMIS / CRS).
"""

from typing import Dict, Any, List, Optional
import pandas as pd


class HealthOutcomeDataset:
    """
    Structured dataset container for paired meteorological-health time series.
    """

    def __init__(self, df: Optional[pd.DataFrame] = None):
        self.df = df

    @classmethod
    def from_records(cls, records: List[Dict[str, Any]]) -> "HealthOutcomeDataset":
        if not records:
            return cls(pd.DataFrame())
        df = pd.DataFrame(records)
        required_cols = ["record_date", "temp_c", "relative_humidity_pct", "utci_c"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required meteorological feature: {col}")
        return cls(df)

    def validate_for_training(self) -> bool:
        """
        Enforce Non-Negotiable Truthfulness Rule:
        Never train ML without genuine verified health labels.
        """
        if self.df is None or self.df.empty:
            raise ValueError("Dataset is empty. Cannot train ML models without genuine health observations.")
        
        target_candidates = ["heat_related_cases", "hospital_admissions", "mortality_count"]
        has_targets = any(col in self.df.columns and self.df[col].notnull().sum() > 30 for col in target_candidates)
        if not has_targets:
            raise ValueError(
                "No genuine health outcome target labels found in dataset. "
                "Training ML on synthetic risk scores is prohibited by SIH26083 truthfulness guidelines."
            )
        return True
