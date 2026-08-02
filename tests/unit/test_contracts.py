from __future__ import annotations

import pytest
from pydantic import ValidationError

from ecosystem.contracts import (
    CapabilityManifest,
    HealthReport,
    OperationalStatus,
    PredictionRequest,
    PredictionResponse,
)


def test_health_report_round_trips_through_json():
    report = HealthReport(domain="lol", status=OperationalStatus.SUCCEEDED, version="2.0.0", details={"a": 1})
    restored = HealthReport.model_validate_json(report.model_dump_json())
    assert restored == report


def test_health_report_rejects_unknown_status():
    with pytest.raises(ValidationError):
        HealthReport(domain="lol", status="NOT_A_REAL_STATUS")


def test_capability_manifest_defaults_are_closed_not_open():
    manifest = CapabilityManifest(domain="cripto")
    assert manifest.supports_prediction is False
    assert manifest.supports_settlement is False
    assert manifest.supports_collection is False


def test_prediction_request_response_round_trip():
    request = PredictionRequest(domain="f1", run_id="abc123", payload={"track": "monza"})
    response = PredictionResponse(
        domain=request.domain,
        run_id=request.run_id,
        status=OperationalStatus.SUCCEEDED,
        payload={"p1": "VER"},
    )
    assert PredictionResponse.model_validate_json(response.model_dump_json()) == response
