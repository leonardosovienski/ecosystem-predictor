"""Contract tests: mechanical compliance checks any real domain adapter
should be able to run against itself. This is the executable half of
docs/adr/0001-plugin-protocol-v1.md - a domain team can point this test
module at their own plugin instance (see the `plugin_under_test` fixture
override pattern) to find out exactly what's missing, instead of reading
prose.
"""

from __future__ import annotations

import pytest

from ecosystem.contracts import CapabilityManifest, HealthReport, OperationalStatus, PluginV1
from tests.fixtures.reference_plugin import ReferencePlugin

pytestmark = pytest.mark.contract


@pytest.fixture
def plugin_under_test() -> PluginV1:
    """Swap this fixture for a real domain's plugin instance to contract-test it.
    Left as the reference implementation here since no real domain plugin can be
    imported from this repository without violating the "no checkout imports
    another" rule."""
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


def test_capabilities_returns_a_typed_manifest_with_matching_domain(plugin_under_test: PluginV1):
    manifest = plugin_under_test.capabilities()
    assert isinstance(manifest, CapabilityManifest)
    assert manifest.domain == plugin_under_test.domain


def test_predict_if_present_accepts_a_plain_dict_and_returns_one(plugin_under_test: PluginV1):
    if not hasattr(plugin_under_test, "predict"):
        pytest.skip(f"{plugin_under_test.domain} does not declare predict() - legitimate, e.g. research-only")
    result = plugin_under_test.predict({"probe": True})
    assert isinstance(result, dict)
