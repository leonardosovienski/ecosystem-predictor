"""Edge cases not covered by the happy-path flows in test_gateway.py:
unknown-domain 404s and the /readyz fail-closed branch when a required
domain is missing."""

from __future__ import annotations

from importlib.metadata import EntryPoint

import pytest
from fastapi.testclient import TestClient

from ecosystem.gateway.app import create_app
from ecosystem.settings import Settings

pytestmark = pytest.mark.e2e

REFERENCE_EP = EntryPoint(
    name="reference", value="tests.fixtures.reference_plugin:ReferencePlugin", group="predictor.plugins"
)
DEGRADED_EP = EntryPoint(
    name="degraded", value="tests.fixtures.reference_plugin:DegradedPlugin", group="predictor.plugins"
)
PREDICTION_DISABLED_EP = EntryPoint(
    name="prediction-disabled",
    value="tests.fixtures.reference_plugin:PredictionDisabledPlugin",
    group="predictor.plugins",
)


@pytest.fixture
def client_with_reference(settings, monkeypatch):
    monkeypatch.setattr("ecosystem.registry.entry_points", lambda group: [REFERENCE_EP])
    with TestClient(create_app(settings)) as test_client:
        yield test_client


def test_health_for_unknown_domain_is_404(client_with_reference, token_factory):
    token = token_factory(scopes="domains:read")
    response = client_with_reference.get(
        "/v1/domains/nonexistent/health", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


def test_capabilities_for_unknown_domain_is_404(client_with_reference, token_factory):
    token = token_factory(scopes="domains:read")
    response = client_with_reference.get(
        "/v1/domains/nonexistent/capabilities", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


def test_capabilities_for_known_domain_reports_prediction_support(client_with_reference, token_factory):
    token = token_factory(scopes="domains:read")
    response = client_with_reference.get(
        "/v1/domains/reference/capabilities", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["supports_prediction"] is True


def test_readyz_fails_closed_when_a_required_domain_is_missing(monkeypatch, settings):
    monkeypatch.setattr("ecosystem.registry.entry_points", lambda group: [])
    settings_with_requirement = settings.model_copy(update={"required_domains": ["reference"]})
    with TestClient(create_app(settings_with_requirement)) as client:
        response = client.get("/readyz")
    assert response.status_code == 503
    assert response.json()["missing_required_domains"] == ["reference"]


def test_readyz_is_ready_when_the_required_domain_loads(settings, monkeypatch):
    monkeypatch.setattr("ecosystem.registry.entry_points", lambda group: [REFERENCE_EP])
    settings_with_requirement: Settings = settings.model_copy(update={"required_domains": ["reference"]})
    with TestClient(create_app(settings_with_requirement)) as client:
        response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_readyz_fails_closed_when_a_required_domain_is_unhealthy(settings, monkeypatch):
    monkeypatch.setattr("ecosystem.registry.entry_points", lambda group: [DEGRADED_EP])
    settings_with_requirement: Settings = settings.model_copy(update={"required_domains": ["degraded"]})
    with TestClient(create_app(settings_with_requirement)) as client:
        response = client.get("/readyz")
    assert response.status_code == 503
    assert response.json()["unhealthy_required_domains"] == ["degraded"]


def test_predict_fails_closed_when_capability_is_disabled(settings, monkeypatch, token_factory):
    monkeypatch.setattr("ecosystem.registry.entry_points", lambda group: [PREDICTION_DISABLED_EP])
    with TestClient(create_app(settings)) as client:
        token = token_factory(scopes="domains:predict")
        response = client.post(
            "/v1/domains/prediction-disabled/predict",
            json={"x": 1},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code == 503
    assert "does not support prediction" in response.json()["detail"]
