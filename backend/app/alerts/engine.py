"""
Alert Generation & Notification Dispatcher for Taapamigo (SIH 2026 PS26083).
Evaluates warning thresholds, formats CAP v1.2 disaster management payloads,
and routes to pluggable notifiers with transparent simulation tracking.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import json
import os
import logging
from .notifiers import get_notifier, get_active_notifiers, BaseNotifier

logger = logging.getLogger(__name__)

_TEMPLATES_CACHE = None


def _load_alert_templates() -> Dict[str, Any]:
    """Load localized alert templates from disk with caching."""
    global _TEMPLATES_CACHE
    if _TEMPLATES_CACHE is not None:
        return _TEMPLATES_CACHE

    candidates = [
        os.path.join(os.getcwd(), "data", "templates", "alert_templates.json"),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "templates", "alert_templates.json")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "templates", "alert_templates.json")),
    ]
    for p in candidates:
        if p and os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    _TEMPLATES_CACHE = json.load(f)
                    return _TEMPLATES_CACHE
            except Exception as e:
                logger.warning(f"Failed loading alert templates from {p}: {e}")

    _TEMPLATES_CACHE = {}
    return _TEMPLATES_CACHE


class AlertDispatcher:
    """
    Generates ITU/WMO CAP v1.2 compliant disaster management warning bulletins
    and manages simulated or active notification dispatches.
    """

    def __init__(self):
        self._dispatch_log: List[Dict[str, Any]] = []

    def generate_alert_payload(
        self,
        city_name: str,
        ward_name: str,
        risk_score: float,
        alert_level: str,
        temp_c: float,
        utci_c: float,
        wbgt_c: float,
        action_summary: str,
        status: str = "Draft"
    ) -> Dict[str, Any]:
        """
        Create ITU/WMO CAP v1.2 JSON emergency alert payload
        while maintaining full backward compatibility with prototype schema.
        """
        alert_level_norm = (alert_level or "YELLOW").upper()
        now = datetime.now(timezone.utc)
        now_iso = now.isoformat()
        clean_city_prefix = "".join(filter(str.isalnum, city_name)).upper()[:3] or "IND"
        alert_id = f"ALERT_{clean_city_prefix}_{now.strftime('%Y%m%d_%H%M%S')}"

        templates_data = _load_alert_templates()
        tmpl_level = templates_data.get("templates", {}).get(alert_level_norm, {})
        en_tmpl = tmpl_level.get("en", {})
        hi_tmpl = tmpl_level.get("hi", {})

        # Format headlines and descriptions
        fmt_params = {
            "city": city_name,
            "ward": ward_name,
            "risk_score": f"{float(risk_score):.1f}",
            "temp_c": f"{float(temp_c):.1f}",
            "utci_c": f"{float(utci_c):.1f}",
            "wbgt_c": f"{float(wbgt_c):.1f}"
        }

        headline_en = en_tmpl.get("headline", f"Heat Stress Advisory for {city_name}").format(**fmt_params)
        desc_en = en_tmpl.get("description", action_summary).format(**fmt_params)
        inst_en = en_tmpl.get("instruction", action_summary).format(**fmt_params)
        sms_en = en_tmpl.get("sms_text", f"TAAPAMIGO ALERT ({alert_level_norm}): {city_name}. {action_summary}").format(**fmt_params)

        # Map alert severity to CAP v1.2 standard severity enumeration
        severity_map = {
            "RED": "Extreme",
            "ORANGE": "Severe",
            "YELLOW": "Moderate",
            "GREEN": "Minor"
        }
        cap_severity = severity_map.get(alert_level_norm, "Moderate")

        cap_info = [
            {
                "language": "en-US",
                "category": "Met",
                "event": "Extreme Heat Wave",
                "responseType": "Prepare" if alert_level_norm == "YELLOW" else "Execute",
                "urgency": "Expected",
                "severity": cap_severity,
                "certainty": "Likely",
                "headline": headline_en,
                "description": desc_en,
                "instruction": inst_en,
                "area": {
                    "areaDesc": f"{ward_name}, {city_name}, India"
                },
                "parameter": [
                    {"valueName": "heat_risk_score", "value": str(round(float(risk_score), 1))},
                    {"valueName": "air_temperature_c", "value": str(round(float(temp_c), 1))},
                    {"valueName": "utci_c", "value": str(round(float(utci_c), 1))},
                    {"valueName": "wbgt_c", "value": str(round(float(wbgt_c), 1))},
                    {"valueName": "review_status", "value": "machine_drafted_needs_native_review"}
                ]
            }
        ]

        if hi_tmpl:
            try:
                headline_hi = hi_tmpl.get("headline", "").format(**fmt_params)
                desc_hi = hi_tmpl.get("description", "").format(**fmt_params)
                inst_hi = hi_tmpl.get("instruction", "").format(**fmt_params)
                cap_info.append({
                    "language": "hi-IN",
                    "category": "Met",
                    "event": "भीषण लू (Heat Wave)",
                    "responseType": "Prepare" if alert_level_norm == "YELLOW" else "Execute",
                    "urgency": "Expected",
                    "severity": cap_severity,
                    "certainty": "Likely",
                    "headline": headline_hi,
                    "description": desc_hi,
                    "instruction": inst_hi,
                    "area": {
                        "areaDesc": f"{ward_name}, {city_name}, भारत"
                    },
                    "parameter": [
                        {"valueName": "review_status", "value": "machine_drafted_needs_native_review"}
                    ]
                })
            except Exception:
                pass

        # Combined CAP v1.2 and backward-compatible root structure
        payload = {
            # Standard OASIS / ITU-T CAP v1.2 Attributes
            "identifier": alert_id,
            "sender": "taapamigo-moes-prototype@gov.in",
            "sent": now_iso,
            "status": status,
            "msgType": "Alert",
            "scope": "Public",
            "info": cap_info,

            # Backward-compatible Prototype API fields
            "alert_id": alert_id,
            "timestamp_utc": now_iso,
            "sms_broadcast_text": sms_en,
            "target": {
                "city": city_name,
                "ward": ward_name
            },
            "metrics": {
                "heat_risk_score": float(risk_score),
                "alert_level": alert_level_norm,
                "temp_c": float(temp_c),
                "utci_c": float(utci_c),
                "wbgt_c": float(wbgt_c)
            },
            "protocols": {
                "action_summary": action_summary,
                "issuing_authority": "Ministry of Earth Sciences (MoES) / NCMRWF & NDMA Prototype",
                "disaster_guideline": "National Action Plan for Heat Related Illnesses (NAP-HRI 2024)",
                "review_status": "machine_drafted_needs_native_review"
            }
        }
        return payload

    def dispatch_mock_webhook(self, webhook_url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate webhook dispatch with explicit SIMULATED_NOT_SENT audit logging.
        """
        log_entry = {
            "dispatched_at": datetime.now(timezone.utc).isoformat(),
            "webhook_url": webhook_url,
            "alert_id": payload.get("alert_id") or payload.get("identifier"),
            "status": "SIMULATED_NOT_SENT",
            "http_code": 200,
            "message": "Simulated webhook delivery (prototype dry-run; no external request made)."
        }
        self._dispatch_log.append(log_entry)
        logger.info(f"Simulated dispatch for alert {log_entry['alert_id']} to {webhook_url}")
        return log_entry

    def dispatch_alert(self, payload: Dict[str, Any], notifier_name: Optional[str] = "console", **kwargs) -> Dict[str, Any]:
        """Dispatch alert through a specified pluggable notifier."""
        notifier = get_notifier(notifier_name or "console", **kwargs)
        result = notifier.send(payload, **kwargs)
        self._dispatch_log.append(result)
        return result

    def get_dispatch_history(self) -> List[Dict[str, Any]]:
        """Return audit history of dispatches during this application runtime."""
        return self._dispatch_log
