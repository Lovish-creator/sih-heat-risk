"""
Pluggable Notifier Interface and Implementations for Taapamigo (SIH 2026 PS26083).

Provides extensible dispatch channels (Console, File, Webhook, SMS)
with transparent status tracking ("SIMULATED_NOT_SENT" in prototype mode).
"""

import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class BaseNotifier(ABC):
    """Abstract Base Class for Alert Notification Channels."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def send(self, payload: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Send or simulate an alert dispatch.
        
        Returns:
            Dictionary containing notifier name, status ('SIMULATED_NOT_SENT' or 'DELIVERED'),
            timestamp, and transport metadata.
        """
        pass


class ConsoleNotifier(BaseNotifier):
    """Outputs alert bulletins to system logger and standard output."""

    def __init__(self):
        super().__init__(name="console")

    def send(self, payload: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        alert_id = payload.get("alert_id") or payload.get("identifier", "UNKNOWN")
        level = payload.get("metrics", {}).get("alert_level") or payload.get("status", "INFO")
        logger.info(f"[ALERT CONSOLE NOTIFIER] Level: {level} | ID: {alert_id} | Payload summary: {payload.get('target', {})}")
        
        return {
            "notifier": self.name,
            "status": "SIMULATED_NOT_SENT",
            "dispatched_at": datetime.now(timezone.utc).isoformat(),
            "alert_id": alert_id,
            "mode": "stdout_logging",
            "message": "Logged alert preview to console/stdout."
        }


class FileNotifier(BaseNotifier):
    """Appends serialized alert records to an offline JSON Lines audit file."""

    def __init__(self, file_path: Optional[str] = None):
        super().__init__(name="file")
        self.file_path = file_path or os.getenv("ALERT_FILE_PATH", "data/alerts/dispatched_alerts.jsonl")

    def send(self, payload: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        alert_id = payload.get("alert_id") or payload.get("identifier", "UNKNOWN")
        record = {
            "record_time_utc": datetime.now(timezone.utc).isoformat(),
            "status": "SIMULATED_NOT_SENT",
            "payload": payload
        }

        # Ensure destination directory exists
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        try:
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            success = True
            msg = f"Appended alert record to {self.file_path}."
        except Exception as e:
            logger.error(f"FileNotifier write failure: {e}")
            success = False
            msg = f"Failed writing to {self.file_path}: {str(e)}"

        return {
            "notifier": self.name,
            "status": "SIMULATED_NOT_SENT",
            "dispatched_at": datetime.now(timezone.utc).isoformat(),
            "alert_id": alert_id,
            "file_path": self.file_path,
            "written_successfully": success,
            "message": msg
        }


class WebhookNotifier(BaseNotifier):
    """Simulates or performs HTTP POST webhook dispatch to municipal disaster EOCs."""

    def __init__(self, default_webhook_url: Optional[str] = None):
        super().__init__(name="webhook")
        self.default_url = default_webhook_url or os.getenv("ALERT_WEBHOOK_URL", "https://mock.ndma.gov.in/eoc/webhook")

    def send(self, payload: Dict[str, Any], webhook_url: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        target_url = webhook_url or self.default_url
        alert_id = payload.get("alert_id") or payload.get("identifier", "UNKNOWN")

        # In Tier-1 working prototype, all webhook dispatches are simulated
        # unless explicit live integration is enabled via environment variables.
        enable_live = os.getenv("ENABLE_LIVE_DISPATCH", "false").lower() in ("true", "1")

        if enable_live and target_url and not target_url.startswith("https://mock"):
            try:
                import urllib.request
                req = urllib.request.Request(
                    target_url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    return {
                        "notifier": self.name,
                        "status": "DELIVERED",
                        "dispatched_at": datetime.now(timezone.utc).isoformat(),
                        "alert_id": alert_id,
                        "webhook_url": target_url,
                        "http_code": response.status
                    }
            except Exception as e:
                logger.warning(f"Live webhook dispatch failed: {e}")
                return {
                    "notifier": self.name,
                    "status": "SIMULATED_NOT_SENT",
                    "dispatched_at": datetime.now(timezone.utc).isoformat(),
                    "alert_id": alert_id,
                    "webhook_url": target_url,
                    "error": str(e)
                }

        return {
            "notifier": self.name,
            "status": "SIMULATED_NOT_SENT",
            "dispatched_at": datetime.now(timezone.utc).isoformat(),
            "alert_id": alert_id,
            "webhook_url": target_url,
            "http_code": 200,
            "message": "Simulated webhook delivery (prototype dry-run)."
        }


class SMSNotifier(BaseNotifier):
    """SMS / C-DAC SACHET Gateway connector requiring institutional credentials."""

    def __init__(self):
        super().__init__(name="sms")
        self.gateway_url = os.getenv("ALERT_SMS_GATEWAY_URL")
        self.api_key = os.getenv("ALERT_SMS_API_KEY")

    def send(self, payload: Dict[str, Any], phone_number: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        alert_id = payload.get("alert_id") or payload.get("identifier", "UNKNOWN")

        if not self.gateway_url or not self.api_key:
            return {
                "notifier": self.name,
                "status": "SIMULATED_NOT_SENT",
                "dispatched_at": datetime.now(timezone.utc).isoformat(),
                "alert_id": alert_id,
                "reason": "unconfigured_gateway_credentials",
                "message": "SMS gateway unconfigured in .env; generated broadcast preview text only."
            }

        return {
            "notifier": self.name,
            "status": "SIMULATED_NOT_SENT",
            "dispatched_at": datetime.now(timezone.utc).isoformat(),
            "alert_id": alert_id,
            "phone_number": phone_number,
            "message": "SMS gateway simulated (Tier-2 institutional connector)."
        }


def get_notifier(name: str, **kwargs) -> BaseNotifier:
    """Factory retrieving a notifier instance by name."""
    n_lower = (name or "console").lower().strip()
    if n_lower == "console":
        return ConsoleNotifier()
    elif n_lower == "file":
        return FileNotifier(file_path=kwargs.get("file_path"))
    elif n_lower == "webhook":
        return WebhookNotifier(default_webhook_url=kwargs.get("webhook_url"))
    elif n_lower == "sms":
        return SMSNotifier()
    else:
        raise ValueError(f"Unknown notifier channel '{name}'. Choose from: console, file, webhook, sms.")


def get_active_notifiers() -> List[BaseNotifier]:
    """Retrieve all active notifiers configured in environment variables."""
    configured = os.getenv("ALERT_NOTIFIERS", "console,file").split(",")
    notifiers = []
    for c in configured:
        c_clean = c.strip()
        if c_clean:
            try:
                notifiers.append(get_notifier(c_clean))
            except ValueError:
                pass
    return notifiers
