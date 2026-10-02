"""
Unit Tests for Alert Generation and Dispatcher.
Validates ITU/WMO CAP v1.2 standard compliance and transparent simulation dispatch.
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

    # Backward compatible fields
    assert "ALERT_ABO_" in payload["alert_id"]
    assert payload["metrics"]["heat_risk_score"] == 86.4
    assert payload["metrics"]["alert_level"] == "RED"
    assert "NAP-HRI" in payload["protocols"]["disaster_guideline"]

    # OASIS / ITU-T CAP v1.2 Standard Compliance
    assert "identifier" in payload
    assert "sender" in payload
    assert "sent" in payload
    assert payload["status"] in ("Draft", "Actual", "Test")
    assert payload["msgType"] == "Alert"
    assert payload["scope"] == "Public"
    assert isinstance(payload["info"], list)
    assert len(payload["info"]) >= 1

    info_en = payload["info"][0]
    assert info_en["category"] == "Met"
    assert "Heat" in info_en["event"]
    assert info_en["severity"] == "Extreme"
    assert "Abohar" in info_en["area"]["areaDesc"]


def test_mock_webhook_dispatch_simulated_status():
    """Verify webhook mock dispatch explicitly records SIMULATED_NOT_SENT."""
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

    # Must be explicitly tagged SIMULATED_NOT_SENT
    assert result["status"] == "SIMULATED_NOT_SENT"
    assert result["http_code"] == 200
    assert len(dispatcher.get_dispatch_history()) >= 1


def test_cap_multilingual_templates():
    """Verify bilingual English and Hindi info blocks are present with review flags."""
    dispatcher = AlertDispatcher()
    payload = dispatcher.generate_alert_payload(
        city_name="Delhi",
        ward_name="Chandni Chowk",
        risk_score=92.0,
        alert_level="RED",
        temp_c=45.2,
        utci_c=49.1,
        wbgt_c=35.2,
        action_summary="Suspension of outdoor work."
    )

    languages = [item.get("language") for item in payload["info"]]
    assert "en-US" in languages
    # Check parameters contain review_status flag
    params = payload["info"][0]["parameter"]
    param_dict = {p["valueName"]: p["value"] for p in params}
    assert param_dict.get("review_status") == "machine_drafted_needs_native_review"
