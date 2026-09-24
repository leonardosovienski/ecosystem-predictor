"""ResearchTaskV2: construction, canonical serialization and fail-closed rejection."""

from __future__ import annotations

import copy
import json

import pytest
from vectors import REQUESTS

from research_protocol import v2
from research_protocol.v2 import V2Error

NOW = "2026-09-24T10:00:00Z"


def make(domain: str, **overrides) -> dict:
    kwargs = {"proposal_id": "cain:PROP-0001", "created_at": NOW}
    kwargs.update(overrides)
    return v2.build_task(domain, copy.deepcopy(REQUESTS[domain]), **kwargs)


def code(exc_info) -> str:
    return exc_info.value.code


def test_build_task_wraps_the_domain_request_and_owns_client_ref(domain):
    task = make(domain)
    request = REQUESTS[domain]
    assert task["domain"] == domain
    assert task["payload_schema"] == f"{domain}-research-request/1"
    assert task["task_id"].startswith(f"{domain}:TASK-") and len(task["task_id"]) == len(domain) + 38
    assert task["payload"]["client_ref"] == {"schema": "research-client-ref/2", "task_id": task["task_id"]}
    assert {k: v for k, v in task["payload"].items() if k != "client_ref"} == request
    # payload_sha256 is the domains' request_content_hash (canonical, without client_ref)
    expected = v2.digest(
        json.dumps(request, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    )
    assert task["payload_sha256"] == expected


def test_task_id_is_deterministic_and_content_bound(domain):
    first, second = (
        make(domain),
        make(domain, proposal_id="cain:PROP-OTHER", created_at="2026-09-25T00:00:00Z"),
    )
    assert first["task_id"] == second["task_id"]
    changed = copy.deepcopy(REQUESTS[domain])
    changed["priority_hint"] = "LOW"
    other = v2.build_task(domain, changed, proposal_id="cain:PROP-0001", created_at=NOW)
    assert other["task_id"] != first["task_id"]
    assert (
        other["request_id"] == first["request_id"]
    )  # same request_id, other content: the domain says CONFLICT


def test_dumps_loads_round_trip_is_byte_identical(domain):
    task = make(domain)
    raw = v2.dumps_task(task)
    assert v2.loads_task(raw) == task
    assert v2.dumps_task(v2.loads_task(raw)) == raw
    assert v2.request_bytes(task) == v2.canonical(task["payload"])


def test_non_canonical_bytes_are_rejected(domain):
    raw = v2.dumps_task(make(domain))
    pretty = json.dumps(json.loads(raw), indent=1, ensure_ascii=False).encode("utf-8")
    with pytest.raises(V2Error) as exc:
        v2.loads_task(pretty)
    assert code(exc) == "NON_CANONICAL"


@pytest.mark.parametrize(
    "raw,expected",
    [
        (b'{"a":1,"a":2}', "SCHEMA_INVALID"),
        (b'{"a":NaN}', "SCHEMA_INVALID"),
        (b"\xff", "SCHEMA_INVALID"),
        (b"[", "SCHEMA_INVALID"),
    ],
)
def test_malformed_json_is_rejected(raw, expected):
    with pytest.raises(V2Error) as exc:
        v2.loads_task(raw)
    assert code(exc) == expected


def test_unknown_field_and_unknown_version_fail_closed(domain):
    task = make(domain)
    extra = dict(task, handler="python -m anything")
    with pytest.raises(V2Error) as exc:
        v2.validate_task(extra)
    assert code(exc) == "UNKNOWN_FIELD"
    for version in ("research-task/1", "research-task/3", "ResearchTaskV1", None):
        with pytest.raises(V2Error) as exc:
            v2.validate_task(dict(task, schema=version))
        assert code(exc) == "VERSION_UNSUPPORTED"


def test_unknown_domain_is_rejected():
    task = make("crypto")
    with pytest.raises(V2Error) as exc:
        v2.validate_task(dict(task, domain="lol"))
    assert code(exc) == "DOMAIN_UNKNOWN"
    with pytest.raises(V2Error) as exc:
        v2.build_task("lol", REQUESTS["crypto"], proposal_id="cain:P", created_at=NOW)
    assert code(exc) == "DOMAIN_UNKNOWN"


def test_payload_must_satisfy_the_contract_request_schema(domain):
    request = copy.deepcopy(REQUESTS[domain])
    request["priority_hint"] = "URGENT"
    with pytest.raises(V2Error) as exc:
        v2.build_task(domain, request, proposal_id="cain:P", created_at=NOW)
    assert code(exc) == "PAYLOAD_INVALID"
    request = copy.deepcopy(REQUESTS[domain])
    request["command"] = "rm -rf /"
    with pytest.raises(V2Error) as exc:
        v2.build_task(domain, request, proposal_id="cain:P", created_at=NOW)
    assert code(exc) == "PAYLOAD_INVALID"


def test_request_of_one_domain_cannot_be_sent_as_another():
    for source in REQUESTS:
        for target in REQUESTS:
            if source == target:
                continue
            with pytest.raises(V2Error) as exc:
                v2.build_task(target, REQUESTS[source], proposal_id="cain:P", created_at=NOW)
            assert code(exc) in {"DOMAIN_MISMATCH", "PAYLOAD_INVALID"}


@pytest.mark.parametrize("bad", ["H9", "Q1", "crypto:H9\n", "crypto: H9", "crypto:", ":H9", "CRYPTO:H9"])
def test_ambiguous_or_unqualified_ids_are_rejected(bad):
    request = copy.deepcopy(REQUESTS["crypto"])
    request["hypothesis_id"] = bad
    with pytest.raises(V2Error) as exc:
        v2.build_task("crypto", request, proposal_id="cain:P", created_at=NOW)
    assert code(exc) in {"ID_NOT_QUALIFIED", "PAYLOAD_INVALID"}


def test_same_local_id_in_three_domains_never_collides():
    tasks = {}
    for domain in REQUESTS:
        request = copy.deepcopy(REQUESTS[domain])
        request["hypothesis_id"] = f"{domain}:H9"
        tasks[domain] = v2.build_task(domain, request, proposal_id="cain:P", created_at=NOW)
    assert len({t["hypothesis_id"] for t in tasks.values()}) == 3
    assert len({t["task_id"] for t in tasks.values()}) == 3


def test_tampering_is_detected(domain):
    task = make(domain)
    changed = copy.deepcopy(task)
    changed["payload"]["priority_hint"] = "HIGH"
    with pytest.raises(V2Error) as exc:
        v2.validate_task(changed)
    assert code(exc) == "PAYLOAD_HASH_MISMATCH"
    changed = copy.deepcopy(task)
    changed["payload"]["client_ref"]["task_id"] = f"{domain}:TASK-" + "0" * 32
    with pytest.raises(V2Error) as exc:
        v2.validate_task(changed)
    assert code(exc) == "CLIENT_REF_MISMATCH"
    changed = copy.deepcopy(task)
    changed["task_id"] = f"{domain}:TASK-" + "0" * 32
    changed["payload"]["client_ref"]["task_id"] = changed["task_id"]
    with pytest.raises(V2Error) as exc:
        v2.validate_task(changed)
    assert code(exc) == "TASK_ID_MISMATCH"
    changed = copy.deepcopy(task)
    changed["research_id"] = f"{domain}:OTHER"
    with pytest.raises(V2Error) as exc:
        v2.validate_task(changed)
    assert code(exc) == "CORRELATION_MISMATCH"


def test_client_ref_belongs_to_the_envelope(domain):
    request = copy.deepcopy(REQUESTS[domain])
    request["client_ref"] = {"anything": 1}
    with pytest.raises(V2Error) as exc:
        v2.build_task(domain, request, proposal_id="cain:P", created_at=NOW)
    assert code(exc) == "CLIENT_REF_RESERVED"


def test_floats_and_non_json_values_are_rejected(domain):
    task = make(domain)
    changed = copy.deepcopy(task)
    changed["payload"]["priority_hint"] = 1.5
    with pytest.raises(V2Error) as exc:
        v2.validate_task(changed)
    assert code(exc) == "FLOAT_FORBIDDEN"


def test_based_on_is_same_domain_only(domain):
    task = make(domain, based_on=[f"{domain}:RESULT-" + "1" * 32])
    assert task["based_on"] == [f"{domain}:RESULT-" + "1" * 32]
    for other in REQUESTS:
        if other != domain:
            with pytest.raises(V2Error) as exc:
                make(domain, based_on=[f"{other}:RESULT-" + "1" * 32])
            assert code(exc) == "DOMAIN_MISMATCH"
    with pytest.raises(V2Error):
        make(domain, based_on=[f"{domain}:X", f"{domain}:X"])


@pytest.mark.parametrize("proposal", ["PROP-1", "crypto:PROP-1", "cain:", 7])
def test_proposal_id_is_cain_qualified(proposal):
    with pytest.raises(V2Error) as exc:
        make("crypto", proposal_id=proposal)
    assert code(exc) == "ID_NOT_QUALIFIED"


@pytest.mark.parametrize(
    "stamp", ["2026-09-24T10:00:00", "2026-09-24T10:00:00+00:00", "2026-09-24 10:00:00Z"]
)
def test_timestamps_are_utc_z(stamp):
    with pytest.raises(V2Error):
        make("crypto", created_at=stamp)


def test_size_limit():
    request = copy.deepcopy(REQUESTS["brasileirao"])
    request["events"]["fixtures"] = [
        {"event_id": i + 1, "kickoff_at": "2024-05-01T19:00:00Z"} for i in range(400)
    ]
    task = v2.build_task("brasileirao", request, proposal_id="cain:P", created_at=NOW)
    assert len(v2.dumps_task(task)) < v2.MAX_TASK_BYTES
    with pytest.raises(V2Error) as exc:
        v2.loads_task(b" " * (v2.MAX_TASK_BYTES + 1))
    assert code(exc) == "SIZE_LIMIT"
