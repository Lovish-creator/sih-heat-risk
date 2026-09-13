"""
Unit Tests for Alert Generation and Dispatcher.
"""

from backend.app.alerts.engine import AlertDispatcher


def test_alert_payload_generation():
    dispatcher = AlertDispatcher()
    payload = dispatcher.generate_alert_payload(
        city_name="Abohar",
        ward_name="Ward 5 - Industrial Area",
        risk_score=86.4,
        alert_level="RED",
        temp_c=43.5,
        utci_c=47.2,
        wbgt_c=34.0,
        action_summary="Halt heavy outdoor work."
    )

    assert "ALERT_ABO_" in payload["alert_id"]
    assert payload["metrics"]["heat_risk_score"] == 86.4
    assert payload["metrics"]["alert_level"] == "RED"
    assert "NAP-HRI" in payload["protocols"]["disaster_guideline"]


def test_mock_webhook_dispatch():
    dispatcher = AlertDispatcher()
    payload = dispatcher.generate_alert_payload(
        city_name="Ahmedabad",
        ward_name="Ward 12",
        risk_score=78.0,
        alert_level="RED",
        temp_c=44.0,
        utci_c=48.0,
        wbgt_c=34.5,
        action_summary="Activate cooling shelters."
    )

    result = dispatcher.dispatch_mock_webhook(
        webhook_url="https://mock.eoc.gujarat.gov.in/alerts",
        payload=payload
    )

    assert result["status"] == "DELIVERED_MOCK"
    assert result["http_code"] == 200
    assert len(dispatcher.get_dispatch_history()) >= 1
