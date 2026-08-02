from __future__ import annotations

from importlib.metadata import EntryPoint

from ecosystem.contracts import OperationalStatus
from ecosystem.registry import Registry

REFERENCE_EP = EntryPoint(
    name="reference", value="tests.fixtures.reference_plugin:ReferencePlugin", group="predictor.plugins"
)
BROKEN_EP = EntryPoint(
    name="broken", value="tests.fixtures.reference_plugin:BrokenPlugin", group="predictor.plugins"
)
MISSING_EP = EntryPoint(
    name="missing", value="tests.fixtures.reference_plugin:DoesNotExist", group="predictor.plugins"
)
ATTRIBUTE_SHAPED_EP = EntryPoint(
    name="attribute-shaped",
    value="tests.fixtures.reference_plugin:AttributeShapedPlugin",
    group="predictor.plugins",
)


def test_discover_loads_a_compliant_plugin(monkeypatch):
    monkeypatch.setattr("ecosystem.registry.entry_points", lambda group: [REFERENCE_EP])
    registry = Registry.discover()

    assert registry.list_domains() == ["reference"]
    record = registry.get("reference")
    assert record.loaded
    assert record.instance.health().status == OperationalStatus.SUCCEEDED


def test_non_compliant_plugin_is_registered_as_degraded_not_dropped(monkeypatch):
    monkeypatch.setattr("ecosystem.registry.entry_points", lambda group: [BROKEN_EP])
    registry = Registry.discover()

    record = registry.get("broken")
    assert record is not None
    assert not record.loaded
    assert "capabilities" in record.error


def test_import_error_does_not_crash_discovery(monkeypatch):
    monkeypatch.setattr("ecosystem.registry.entry_points", lambda group: [MISSING_EP])
    registry = Registry.discover()

    record = registry.get("missing")
    assert record is not None
    assert not record.loaded


def test_health_snapshot_reports_failed_for_unloaded_plugin(monkeypatch):
    monkeypatch.setattr("ecosystem.registry.entry_points", lambda group: [BROKEN_EP])
    registry = Registry.discover()

    snapshot = registry.health_snapshot()
    assert snapshot["broken"].status == OperationalStatus.FAILED


def test_attribute_shaped_capabilities_is_rejected_at_load_not_call_time(monkeypatch):
    """Regression test for lol-predictor's real current shape (see
    docs/adr/0001-plugin-protocol-v1.md): `capabilities` as a plain
    attribute, not a method, must be caught by discovery itself."""
    monkeypatch.setattr("ecosystem.registry.entry_points", lambda group: [ATTRIBUTE_SHAPED_EP])
    registry = Registry.discover()

    record = registry.get("attribute-shaped")
    assert record is not None
    assert not record.loaded
    assert "callable" in record.error


def test_mixed_registry_loads_good_and_degrades_bad_independently(monkeypatch):
    monkeypatch.setattr("ecosystem.registry.entry_points", lambda group: [REFERENCE_EP, BROKEN_EP])
    registry = Registry.discover()

    assert registry.get("reference").loaded
    assert not registry.get("broken").loaded
