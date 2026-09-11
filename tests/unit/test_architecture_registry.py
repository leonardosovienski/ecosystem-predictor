from importlib.metadata import EntryPoint

import pytest

from ecosystem.registry import PluginRecord, Registry


@pytest.mark.parametrize("reverse", [False, True])
def test_duplicate_names_never_execute_plugin_code(monkeypatch, reverse):
    first = EntryPoint(name="duplicate", value="missing:first", group="predictor.plugins")
    second = EntryPoint(name="duplicate", value="missing:second", group="predictor.plugins")
    monkeypatch.setattr(
        "ecosystem.registry.entry_points", lambda group: [second, first] if reverse else [first, second]
    )
    monkeypatch.setattr(EntryPoint, "load", lambda self: (_ for _ in ()).throw(AssertionError("loaded")))
    registry = Registry.discover()
    assert not registry.records["duplicate"].loaded
    assert registry.records["duplicate"].error == "duplicate entry-point name"


def test_invalid_state_retains_literal_producer_payload():
    class Producer:
        def capabilities(self):
            return {"domain": "stocks", "scientific_status": "REJECTED_BY_PROTOCOL"}

        def health(self):
            return {"domain": "stocks", "status": "SUCCEEDED"}

    ep = EntryPoint(name="stocks", value="unused:Producer", group="predictor.plugins")
    registry = Registry(records={"stocks": PluginRecord("stocks", ep, Producer())})
    result = registry.diagnostic_snapshot()["stocks"]
    assert result["capabilities"]["contract_status"] == "INVALID"
    assert result["capabilities"]["payload"]["scientific_status"] == "REJECTED_BY_PROTOCOL"
    assert result["health"]["contract_status"] == "VALID"


@pytest.mark.parametrize("state", ["NO_ACTIVE_HYPOTHESIS", "ACTIVE_HYPOTHESIS", "DISCOVERY_INCONCLUSIVE"])
def test_native_states_have_a_domain_namespace_without_semantic_translation(state):
    class Producer:
        def capabilities(self):
            return {
                "domain": "crypto",
                "scientific_status": state,
                "predictive_status": "INCONCLUSIVE",
                "economic_status": "HISTORICAL_NO_GO",
                "capital_permission": "FORBIDDEN",
                "supports_prediction": False,
                "supports_settlement": False,
                "supports_collection": False,
            }

        def health(self):
            return {"domain": "crypto", "status": "WAITING"}

    ep = EntryPoint(name="cripto", value="unused:Producer", group="predictor.plugins")
    registry = Registry(records={"cripto": PluginRecord("cripto", ep, Producer())})
    result = registry.diagnostic_snapshot()["cripto"]
    report = result["capabilities"]
    assert report["contract_status"] == "VALID"
    assert report["state_namespace"] == "crypto"
    assert report["state_mapping"] is None
    assert report["payload"]["scientific_status"] == state
    assert result["capital_authorized_by_diagnostic"] is False
