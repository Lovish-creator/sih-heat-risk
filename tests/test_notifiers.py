"""
Unit Tests for Pluggable Notifier Channels (Console, File, Webhook, SMS).
"""

import os
import json
import pytest
from backend.app.alerts.notifiers import (
    ConsoleNotifier,
    FileNotifier,
    WebhookNotifier,
    SMSNotifier,
    get_notifier,
    get_active_notifiers
)


@pytest.fixture
def sample_payload():
    return {
        "identifier": "TEST_ALERT_001",
        "alert_id": "TEST_ALERT_001",
        "status": "Draft",
        "target": {"city": "Ahmedabad", "ward": "Ward 1"},
        "metrics": {"alert_level": "RED", "heat_risk_score": 88.0}
    }


def test_console_notifier(sample_payload):
    notifier = ConsoleNotifier()
    res = notifier.send(sample_payload)
    assert res["status"] == "SIMULATED_NOT_SENT"
    assert res["notifier"] == "console"
    assert res["alert_id"] == "TEST_ALERT_001"


def test_file_notifier(sample_payload, tmp_path):
    test_file = str(tmp_path / "test_alerts.jsonl")
    notifier = FileNotifier(file_path=test_file)
    res = notifier.send(sample_payload)

    assert res["status"] == "SIMULATED_NOT_SENT"
    assert res["notifier"] == "file"
    assert os.path.exists(test_file)

    with open(test_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["status"] == "SIMULATED_NOT_SENT"
    assert record["payload"]["alert_id"] == "TEST_ALERT_001"


def test_webhook_notifier_simulation(sample_payload):
    notifier = WebhookNotifier()
    res = notifier.send(sample_payload, webhook_url="https://mock.ndma.gov.in/eoc/webhook")
    assert res["status"] == "SIMULATED_NOT_SENT"
    assert res["notifier"] == "webhook"
    assert res["http_code"] == 200


def test_sms_notifier_unconfigured(sample_payload, monkeypatch):
    monkeypatch.delenv("ALERT_SMS_GATEWAY_URL", raising=False)
    monkeypatch.delenv("ALERT_SMS_API_KEY", raising=False)
    notifier = SMSNotifier()
    res = notifier.send(sample_payload)
    assert res["status"] == "SIMULATED_NOT_SENT"
    assert res["notifier"] == "sms"
    assert res["reason"] == "unconfigured_gateway_credentials"


def test_notifier_factory():
    console = get_notifier("console")
    assert isinstance(console, ConsoleNotifier)

    file_notif = get_notifier("file")
    assert isinstance(file_notif, FileNotifier)

    with pytest.raises(ValueError):
        get_notifier("nonexistent_notifier")


def test_active_notifiers(monkeypatch):
    monkeypatch.setenv("ALERT_NOTIFIERS", "console,file")
    active = get_active_notifiers()
    names = [n.name for n in active]
    assert "console" in names
    assert "file" in names
