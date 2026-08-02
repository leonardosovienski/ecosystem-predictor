"""End-to-end: a real FastAPI app, a real (fixture) plugin discovered
through the real registry mechanism, real JWT tokens - only the network
transport is skipped (TestClient calls the ASGI app in-process). No
OpenTelemetry OTLP endpoint is configured, so tracing exports to a
ConsoleSpanExporter for the duration of the test - loud but harmless."""

from __future__ import annotations

from importlib.metadata import EntryPoint

import pytest
from fastapi.testclient import TestClient

from ecosystem.gateway.app import create_app

pytestmark = pytest.mark.e2e

REFERENCE_EP = EntryPoint(
    name="reference", value="tests.fixtures.reference_plugin:ReferencePlugin", group="predictor.plugins"
)


@pytest.fixture
def client(settings, monkeypatch):
    monkeypatch.setattr("ecosystem.registry.entry_points", lambda group: [REFERENCE_EP])
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client


def test_healthz_requires_no_auth(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readyz_reports_ready_with_no_required_domains(client):
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_domains_endpoint_requires_a_bearer_token(client):
    response = client.get("/v1/domains")
    assert response.status_code == 401


def test_domains_endpoint_lists_the_discovered_plugin(client, token_factory):
    token = token_factory(scopes="domains:read")
    response = client.get("/v1/domains", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == ["reference"]


def test_predict_without_scope_is_forbidden(client, token_factory):
    token = token_factory(scopes="domains:read")
    response = client.post(
        "/v1/domains/reference/predict", json={"x": 1}, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_predict_dispatches_to_the_loaded_plugin(client, token_factory):
    token = token_factory(scopes="domains:predict")
    response = client.post(
        "/v1/domains/reference/predict", json={"x": 1}, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["domain"] == "reference"
    assert body["payload"] == {"echo": {"x": 1}}


def test_predict_on_unknown_domain_fails_closed_with_503(client, token_factory):
    token = token_factory(scopes="domains:predict")
    response = client.post(
        "/v1/domains/nonexistent/predict", json={}, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 503
