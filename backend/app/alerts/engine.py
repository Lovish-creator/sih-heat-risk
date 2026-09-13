"""
Alert Generation & Notification Dispatcher.
Evaluates warning thresholds and dispatches structured JSON payloads to registered webhooks.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import logging
import json

from ..core.constants import AlertLevel

logger = logging.getLogger(__name__)


class AlertDispatcher:
    """
    Generates and formats disaster management warning bulletins for municipal emergency operations centers.
    """

    def __init__(self):
        self._dispatch_log = []

    def generate_alert_payload(
        self,
        city_name: str,
        ward_name: str,
        risk_score: float,
        alert_level: str,
        temp_c: float,
        utci_c: float,
        wbgt_c: float,
        action_summary: str
    ) -> Dict[str, Any]:
        """Create structured JSON alert message."""
        return {
            "alert_id": f"ALERT_{city_name.upper()[:3]}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "target": {
                "city": city_name,
                "ward": ward_name
            },
            "metrics": {
                "heat_risk_score": float(risk_score),
                "alert_level": alert_level,
                "temp_c": float(temp_c),
                "utci_c": float(utci_c),
                "wbgt_c": float(wbgt_c)
            },
            "protocols": {
                "action_summary": action_summary,
                "issuing_authority": "Ministry of Earth Sciences (MoES) / NCMRWF & NDMA Prototype",
                "disaster_guideline": "National Action Plan for Heat Related Illnesses (NAP-HRI 2024)"
            }
        }

    def dispatch_mock_webhook(self, webhook_url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate webhook dispatch with audit logging.
        """
        log_entry = {
            "dispatched_at": datetime.now(timezone.utc).isoformat(),
            "webhook_url": webhook_url,
            "alert_id": payload.get("alert_id"),
            "status": "DELIVERED_MOCK",
            "http_code": 200
        }
        self._dispatch_log.append(log_entry)
        logger.info(f"Dispatched alert {payload.get('alert_id')} to {webhook_url}")
        return log_entry

    def get_dispatch_history(self) -> List[Dict[str, Any]]:
        return self._dispatch_log
