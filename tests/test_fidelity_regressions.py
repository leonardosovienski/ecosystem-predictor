from datetime import UTC, datetime
from importlib.metadata import EntryPoint

import pytest

from ecosystem.registry import PluginRecord, Registry
from tests.test_ecosystem_drift import drift


@pytest.mark.parametrize(
    ("expires", "invalid"),
    [
        ("2026-09-13T16:42:06Z", True),
        ("2026-09-13T16:42:07Z", False),
        ("2026-09-13T13:42:06-03:00", True),
        ("2026-09-13", True),
        ("UNKNOWN", True),
        (None, True),
    ],
)
def test_expiry_checks_exact_instant_and_requires_timezone(expires, invalid):
    item = {"repo": "synthetic", "status": "ALIGNED", "expires_at": expires}
    assert bool(drift.check_expiry(item, datetime(2026, 9, 13, 16, 42, 6, tzinfo=UTC))) is invalid


def test_historical_expiry_is_not_recertified():
    item = {"repo": "synthetic", "status": "EXPIRED", "expires_at": "2026-09-13T16:42:06Z"}
    assert drift.check_expiry(item, datetime(2026, 9, 14, tzinfo=UTC)) == []


def test_plugin_exception_messages_never_escape(caplog, monkeypatch):
    marker = "SYNTHETIC_PRIVATE_VALUE"

    def broken(*args):
        raise RuntimeError(marker)

    ep = EntryPoint(name="synthetic", value="synthetic:plugin", group="predictor.plugins")
    monkeypatch.setattr(EntryPoint, "load", broken)
    registry = Registry()
    registry._load_one(ep)
    assert marker not in caplog.text
    assert registry.records["synthetic"].error == "RuntimeError"
    assert marker not in repr(registry.health_snapshot())
    assert marker not in repr(registry.capability_snapshot())

    class Broken:
        health = broken
        capabilities = broken

    registry.records["synthetic"] = PluginRecord(name="synthetic", entry_point=ep, instance=Broken())
    assert "RuntimeError" in repr(registry.health_snapshot())
    assert marker not in repr(registry.health_snapshot())
    assert marker not in repr(registry.capability_snapshot())
    assert marker not in repr(registry.diagnostic_snapshot())
