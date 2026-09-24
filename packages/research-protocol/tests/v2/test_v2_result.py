"""ResearchResultV2: byte-identical domain payload, correlation and fail-closed rejection."""

from __future__ import annotations

import copy
import json

import pytest
from vectors import ADAPTER, REQUESTS, outcome

from research_protocol import v2
from research_protocol.v2 import V2Error

NOW = "2026-09-24T10:00:02Z"


def task_for(domain: str, request_id: str = "") -> dict:
    request = copy.deepcopy(REQUESTS[domain])
    if request_id:
        request["request_id"] = request_id
    return v2.build_task(domain, request, proposal_id="cain:PROP-0001", created_at="2026-09-24T10:00:00Z")


def wrap(task: dict, out: dict) -> dict:
    return v2.build_result(task, out, adapter=dict(ADAPTER), produced_at=NOW)


def code(exc_info) -> str:
    return exc_info.value.code


def test_result_carries_the_domain_result_byte_identical(domain):
    task = task_for(domain)
    out = outcome(domain, task)
    result = wrap(task, out)
    expected = json.dumps(
        out["result"], sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")
    assert v2.domain_payload(result) == expected
    assert result["result"]["payload_sha256"] == v2.digest(expected)
    assert result["client_ref"] == task["payload"]["client_ref"]
    for field in ("result_state", "operational_state", "scientific_state", "economic_state"):
        assert result["result"][field] == out["result"][field]  # carried as-is, never promoted
    assert result["result"]["capital_permission"] is False


def test_round_trip_is_canonical_and_floats_stay_inside_the_payload(domain):
    task = task_for(domain)
    result = wrap(task, outcome(domain, task))
    raw = v2.dumps_result(result, task=task)
    assert v2.loads_result(raw, task=task) == result
    assert v2.dumps_result(v2.loads_result(raw)) == raw
    assert "0.30000000000000004" in result["result"]["payload_canonical"]


@pytest.mark.parametrize(
    "status",
    [
        "REJECTED",
        "CONFLICT",
        "NOT_READY",
        "OPS_FAILED_RETRYABLE",
        "TEMPORAL_INTEGRITY_VIOLATION",
        "RECONCILIATION_REQUIRED",
    ],
)
def test_non_result_outcomes_carry_no_result(domain, status):
    task = task_for(domain)
    result = wrap(task, outcome(domain, task, status))
    assert result["result"] is None
    assert result["outcome"]["status"] == status
    assert v2.OUTCOME_CLASSES[status] in {"TERMINAL_REFUSAL", "RETRYABLE", "REQUIRES_HUMAN"}


def test_stocks_only_statuses_are_domain_bound():
    task = task_for("stocks")
    assert wrap(task, outcome("stocks", task, "STATE_BUSY_RETRYABLE"))["result"] is None
    for domain in ("crypto", "brasileirao"):
        other = task_for(domain)
        with pytest.raises(V2Error) as exc:
            wrap(other, outcome(domain, other, "STATE_BUSY_RETRYABLE"))
        assert code(exc) == "OUTCOME_INVALID"


def test_rejected_before_parsing_may_lack_client_ref(domain):
    task = task_for(domain)
    out = outcome(domain, task, "REJECTED")
    del out["client_ref"]
    out["request_id"] = None
    assert wrap(task, out)["client_ref"] is None
    out = outcome(domain, task, "RESULT")
    del out["client_ref"]
    with pytest.raises(V2Error) as exc:
        wrap(task, out)
    assert code(exc) == "CLIENT_REF_MISMATCH"


def test_result_of_one_domain_never_satisfies_a_task_of_another():
    tasks = {d: task_for(d) for d in REQUESTS}
    results = {d: wrap(t, outcome(d, t)) for d, t in tasks.items()}
    for source, result in results.items():
        for target, task in tasks.items():
            if source == target:
                assert v2.validate_result(result, task=task) is result
            else:
                with pytest.raises(V2Error) as exc:
                    v2.validate_result(result, task=task)
                assert code(exc) == "DOMAIN_MISMATCH"


def test_result_of_another_task_in_the_same_domain_is_rejected(domain):
    first = task_for(domain)
    second = task_for(domain, request_id=f"{domain}:REQ-0002")
    result = wrap(first, outcome(domain, first))
    with pytest.raises(V2Error) as exc:
        v2.validate_result(result, task=second)
    assert code(exc) == "TASK_MISMATCH"


def test_payload_tampering_is_detected(domain):
    task = task_for(domain)
    result = wrap(task, outcome(domain, task))
    body = result["result"]
    changed = copy.deepcopy(result)
    changed["result"]["payload_canonical"] = body["payload_canonical"].replace('"NO_EDGE"', '"WATCH"', 1)
    with pytest.raises(V2Error) as exc:
        v2.validate_result(changed)
    assert code(exc) == "PAYLOAD_HASH_MISMATCH"
    # re-hashed tampering is caught by the header/payload correlation
    changed["result"]["payload_sha256"] = v2.digest(changed["result"]["payload_canonical"].encode())
    with pytest.raises(V2Error):
        v2.validate_result(changed)
    # a non-canonical rendering of the same result is rejected
    pretty = json.dumps(json.loads(body["payload_canonical"]), indent=1, ensure_ascii=False)
    changed = copy.deepcopy(result)
    changed["result"]["payload_canonical"] = pretty
    changed["result"]["payload_sha256"] = v2.digest(pretty.encode())
    with pytest.raises(V2Error) as exc:
        v2.validate_result(changed)
    assert code(exc) == "NON_CANONICAL"


def test_header_states_cannot_be_promoted(domain):
    task = task_for(domain)
    result = wrap(task, outcome(domain, task))
    changed = copy.deepcopy(result)
    changed["result"]["economic_state"] = "WATCH"
    with pytest.raises(V2Error) as exc:
        v2.validate_result(changed)
    assert code(exc) == "CORRELATION_MISMATCH"
    changed = copy.deepcopy(result)
    changed["result"]["capital_permission"] = True
    with pytest.raises(V2Error) as exc:
        v2.validate_result(changed)
    assert code(exc) == "CAPITAL_FORBIDDEN"


def test_domain_result_granting_capital_is_rejected(domain):
    task = task_for(domain)
    out = outcome(domain, task)
    out["result"]["capital_permission"] = True
    with pytest.raises(V2Error) as exc:
        wrap(task, out)
    assert code(exc) == "CAPITAL_FORBIDDEN"


def test_domain_result_with_foreign_ids_or_unknown_states_is_rejected(domain):
    task = task_for(domain)
    other = next(d for d in REQUESTS if d != domain)
    out = outcome(domain, task)
    out["result"]["result_id"] = f"{other}:RESULT-" + "a" * 32
    out["result_id"] = out["result"]["result_id"]
    with pytest.raises(V2Error) as exc:
        wrap(task, out)
    assert code(exc) == "DOMAIN_MISMATCH"
    out = outcome(domain, task)
    out["result"]["scientific_state"] = "PROVEN_EDGE"
    out["scientific_state"] = "PROVEN_EDGE"
    with pytest.raises(V2Error) as exc:
        wrap(task, out)
    assert code(exc) == "PAYLOAD_INVALID"
    out = outcome(domain, task)
    out["result"]["extra"] = 1
    with pytest.raises(V2Error) as exc:
        wrap(task, out)
    assert code(exc) == "PAYLOAD_INVALID"


def test_outcome_must_match_its_result(domain):
    task = task_for(domain)
    out = outcome(domain, task)
    out["result_state"] = "WATCH_NO_CAPITAL"
    with pytest.raises(V2Error) as exc:
        wrap(task, out)
    assert code(exc) == "CORRELATION_MISMATCH"
    out = outcome(domain, task)
    out["exit_code"] = 3
    with pytest.raises(V2Error) as exc:
        wrap(task, out)
    assert code(exc) == "OUTCOME_INVALID"
    out = outcome(domain, task, "REJECTED")
    out["result"] = {}
    with pytest.raises(V2Error) as exc:
        wrap(task, out)
    assert code(exc) == "OUTCOME_INVALID"
    out = outcome(domain, task)
    out["request_id"] = f"{domain}:REQ-OTHER"
    with pytest.raises(V2Error) as exc:
        wrap(task, out)
    assert code(exc) == "CORRELATION_MISMATCH"


def test_unknown_field_version_and_non_canonical_result_bytes(domain):
    task = task_for(domain)
    result = wrap(task, outcome(domain, task))
    with pytest.raises(V2Error) as exc:
        v2.validate_result(dict(result, capital="granted"))
    assert code(exc) == "UNKNOWN_FIELD"
    with pytest.raises(V2Error) as exc:
        v2.validate_result(dict(result, schema="research-result/1"))
    assert code(exc) == "VERSION_UNSUPPORTED"
    raw = v2.dumps_result(result)
    with pytest.raises(V2Error) as exc:
        v2.loads_result(raw + b"\n")
    assert code(exc) in {"NON_CANONICAL", "SCHEMA_INVALID"}
    with pytest.raises(V2Error) as exc:
        v2.loads_result(json.dumps(json.loads(raw), indent=2).encode())
    assert code(exc) == "NON_CANONICAL"


def test_duplicate_outcome_is_equivalent_to_the_first_result(domain):
    task = task_for(domain)
    first = wrap(task, outcome(domain, task, "RESULT"))
    dup = wrap(task, outcome(domain, task, "DUPLICATE"))
    assert dup["result"] == first["result"]
    assert v2.domain_payload(dup) == v2.domain_payload(first)
