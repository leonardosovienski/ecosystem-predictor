"""The packaged domain registry mirrors the three DOMAIN_RESEARCH_CONTRACT.json."""

from __future__ import annotations

import re

from research_protocol import v2


def test_three_domains_with_their_own_prefixes():
    assert v2.DOMAINS == ("brasileirao", "crypto", "stocks")
    for name, entry in v2.REGISTRY["domains"].items():
        assert entry["request_schema_id"] == f"{name}-research-request/1"
        assert entry["result_schema_id"] == f"{name}-research-result/1"
        assert entry["contract"]["path"] == f"qualification/{name}/DOMAIN_RESEARCH_CONTRACT.json"
        assert re.fullmatch(r"[0-9a-f]{64}", entry["contract"]["sha256"])
        assert entry["adapter_paths"] and all(p.endswith("/adapters/") for p in entry["adapter_paths"])
        # every ID the request schema declares is qualified with this domain only
        for definition in entry["request_schema"]["$defs"].values():
            pattern = definition.get("pattern", "")
            if pattern.endswith(":[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$"):
                assert pattern.startswith(f"^{name}:")


def test_outcome_statuses_and_exit_codes():
    for entry in v2.REGISTRY["domains"].values():
        codes = entry["outcome_exit_codes"]
        assert {
            "RESULT",
            "DUPLICATE",
            "REJECTED",
            "CONFLICT",
            "NOT_READY",
            "OPS_FAILED_RETRYABLE",
            "TEMPORAL_INTEGRITY_VIOLATION",
            "RECONCILIATION_REQUIRED",
        } <= set(codes)
        assert set(codes) <= set(v2.OUTCOME_CLASSES)
        assert codes["RESULT"] == codes["DUPLICATE"] == 0


def test_capital_is_never_a_state():
    for entry in v2.REGISTRY["domains"].values():
        states = entry["result_states"] + entry["economic_states"]
        assert not any("CAPITAL" in s and s != "WATCH_NO_CAPITAL" for s in states)
        assert "capital_permission" in entry["result_required_fields"]


def test_registry_sha256_is_exposed():
    assert re.fullmatch(r"[0-9a-f]{64}", v2.REGISTRY_SHA256)
    assert re.fullmatch(r"[0-9a-f]{40}", v2.REGISTRY["source"]["commit"])
