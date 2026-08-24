"""Executable contract checks for PluginV1 adapters."""

from __future__ import annotations

import pytest

from ecosystem.contracts import (
    CapabilityManifest,
    CapitalPermission,
    EconomicStatus,
    HealthReport,
    OperationalStatus,
    PluginV1,
    PredictiveStatus,
    ScientificStatus,
)
from tests.fixtures.reference_plugin import ReferencePlugin

pytestmark = pytest.mark.contract


@pytest.fixture
def plugin_under_test() -> PluginV1:
    return ReferencePlugin()


def test_plugin_satisfies_the_v1_protocol(plugin_under_test: PluginV1):
    assert isinstance(plugin_under_test, PluginV1)


def test_domain_attribute_is_a_non_empty_string(plugin_under_test: PluginV1):
    assert isinstance(plugin_under_test.domain, str) and plugin_under_test.domain


def test_health_returns_a_typed_report_with_matching_domain(plugin_under_test: PluginV1):
    report = plugin_under_test.health()
    assert isinstance(report, HealthReport)
    assert report.domain == plugin_under_test.domain
    assert isinstance(report.status, OperationalStatus)


def test_capabilities_returns_canonical_orthogonal_states(plugin_under_test: PluginV1):
    manifest = plugin_under_test.capabilities()
    assert isinstance(manifest, CapabilityManifest)
    assert manifest.domain == plugin_under_test.domain
    assert isinstance(manifest.scientific_status, ScientificStatus)
    assert isinstance(manifest.predictive_status, PredictiveStatus)
    assert isinstance(manifest.economic_status, EconomicStatus)
    assert isinstance(manifest.capital_permission, CapitalPermission)
    assert manifest.supports_no_opportunity is True


def test_missing_state_fails_closed_by_default():
    manifest = CapabilityManifest(domain="research-only")
    assert manifest.scientific_status is ScientificStatus.UNKNOWN
    assert manifest.predictive_status is PredictiveStatus.UNKNOWN
    assert manifest.economic_status is EconomicStatus.UNKNOWN
    assert manifest.capital_permission is CapitalPermission.FORBIDDEN
    assert manifest.supports_no_opportunity is True


def test_predict_if_present_accepts_a_plain_dict_and_returns_one(plugin_under_test: PluginV1):
    if not hasattr(plugin_under_test, "predict"):
        pytest.skip(f"{plugin_under_test.domain} does not declare predict()")
    result = plugin_under_test.predict({"probe": True})
    assert isinstance(result, dict)
