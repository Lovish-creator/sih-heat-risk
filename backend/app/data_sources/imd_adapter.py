"""
India Meteorological Department (IMD) Guidance & Thresholds Adapter.

Provides programmatic access to official Indian heatwave criteria,
climatological departures, and 4-tier warning definitions.
"""

from typing import Dict, Any, Optional


class IMDGuidanceAdapter:
    """
    Encapsulates IMD official heatwave criteria and district warning guidelines.
    Reference: https://mausam.imd.gov.in/responsive/heatwave_guidance.php
    """

    @staticmethod
    def evaluate_imd_heatwave(
        max_temp_c: float,
        normal_temp_c: float = 40.0,
        region_type: str = "plains"
    ) -> Dict[str, Any]:
        """
        Evaluate official IMD heatwave criteria based on absolute temperature and normal departure.
        
        Args:
            max_temp_c: Maximum dry-bulb temperature in Celsius.
            normal_temp_c: Climatological normal temperature for the station/month.
            region_type: 'plains', 'coastal', or 'hilly'.
            
        Returns:
            Dictionary with heatwave status, severe status, departure, and IMD color code.
        """
        t = float(max_temp_c)
        t_norm = float(normal_temp_c)
        departure = round(t - t_norm, 1)

        reg = region_type.lower()
        is_heatwave = False
        is_severe = False

        if reg == "plains":
            # Plains criteria: Max temp >= 40 C
            if t >= 40.0:
                if departure >= 6.5 or t >= 47.0:
                    is_heatwave = True
                    is_severe = True
                elif departure >= 4.5 or t >= 45.0:
                    is_heatwave = True
        elif reg == "coastal":
            if t >= 37.0:
                if departure >= 6.5:
                    is_heatwave = True
                    is_severe = True
                elif departure >= 4.5:
                    is_heatwave = True
        else: # hilly
            if t >= 30.0:
                if departure >= 6.5:
                    is_heatwave = True
                    is_severe = True
                elif departure >= 4.5:
                    is_heatwave = True

        if is_severe:
            alert_color = "RED"
            alert_label = "Severe Heat Wave Alert"
        elif is_heatwave:
            alert_color = "ORANGE"
            alert_label = "Heat Wave Alert"
        elif t >= 40.0:
            alert_color = "YELLOW"
            alert_label = "Hot Day / Watch"
        else:
            alert_color = "GREEN"
            alert_label = "No Warning"

        return {
            "max_temp_c": t,
            "climatological_normal_c": t_norm,
            "departure_from_normal_c": departure,
            "is_heatwave": is_heatwave,
            "is_severe_heatwave": is_severe,
            "region_type": reg,
            "imd_alert_level": alert_color,
            "imd_alert_label": alert_label,
            "source": "IMD Heat Wave Guidance Methodology"
        }
