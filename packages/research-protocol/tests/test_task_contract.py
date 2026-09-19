import unicodedata
from copy import deepcopy

import pytest
from research_protocol import (
    TASK_VERSION,
    canonical,
    digest,
    payload_hash,
    sign_task,
    validate_task,
    verify_task,
)

SECRET = bytes.fromhex("11" * 32)


def task():
    def ref(kind, name):
        return {"kind": kind, "name": name, "version": "v1"}

    return {
        "schema_version": "ResearchTaskV1",
        "task_id": "TASK-001",
        "research_id": "RESEARCH-001",
        "parent_task_id": None,
        "hypothesis_id": "H6",
        "domain": "crypto",
        "request_type": "BACKTEST_EXISTING_HYPOTHESIS",
        "protocol_ref": ref("protocol", "backtest-standard"),
        "dataset_constraint_ref": ref("dataset", "btc-daily-pit"),
        "baseline_refs": [ref("baseline", "majority-direction")],
        "cost_model_ref": ref("cost_model", "spot-standard"),
        "evidence_refs": [ref("evidence", "cain-receipt-001")],
        "bounded_parameters": {
            "symbol": "BTCUSDT",
            "horizon_days": 7,
            "max_observations": 500,
            "fee_bps": 10,
            "slippage_bps": 5,
        },
        "priority_hint": "HIGH",
        "created_at": "2026-09-19T22:30:00Z",
        "expires_at": "2026-09-20T22:30:00Z",
        "requested_by": "qa-cain-f3",
        "provenance": {
            "cain_source_sha": "6f9d254776b2a3c251f6cce14529087c57ebbeae",
            "retrieval_receipt_ids": ["receipt-001"],
            "proposal_model": "deterministic-fixture",
        },
    }


def signed(value=None):
    return sign_task(
        value or task(),
        producer="CAIN",
        publisher_identity="cain-qa",
        consumer="CRIPTO",
        scope="crypto.research.propose",
        key_id="cain-f3-key",
        secret=SECRET,
    )


def test_canonical_hash_ignores_key_order_and_uses_nfc():
    first = {"b": 1, "a": unicodedata.normalize("NFD", "ação")}
    second = {"a": "ação", "b": 1}
    assert canonical(first) == canonical(second)
    reversed_task = dict(reversed(list(task().items())))
    assert payload_hash(task()) == payload_hash(reversed_task)
    changed = task()
    changed["bounded_parameters"]["fee_bps"] += 1
    assert payload_hash(task()) != payload_hash(changed)


def test_task_and_signature_roundtrip():
    envelope = signed()
    assert verify_task(envelope, lambda publisher, key: SECRET) == envelope


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value.update(command="powershell.exe"),
        lambda value: value.update(request_type="ARBITRARY_PYTHON"),
        lambda value: value["bounded_parameters"].update(extra="rm -rf"),
        lambda value: value["bounded_parameters"].update(fee_bps=1.5),
        lambda value: value["bounded_parameters"].update(max_observations=1_000_000),
        lambda value: value["protocol_ref"].update(name="../escape"),
        lambda value: value["protocol_ref"].update(url="http://127.0.0.1/secret"),
        lambda value: value.update(expires_at=value["created_at"]),
        lambda value: value.update(priority_hint="ABSOLUTE"),
        lambda value: value["provenance"].update(api_key="secret"),
    ],
)
def test_task_fails_closed(mutation):
    value = task()
    mutation(value)
    with pytest.raises(ValueError):
        validate_task(value)


def test_forged_unknown_and_revoked_keys_fail_closed():
    envelope = signed()
    forged = deepcopy(envelope)
    forged["payload"]["bounded_parameters"]["fee_bps"] = 11
    forged["payload_hash"] = payload_hash(forged["payload"])
    forged["message_id"] = digest(
        canonical([TASK_VERSION, forged["payload"]["task_id"], forged["payload_hash"]])
    )
    with pytest.raises(PermissionError):
        verify_task(forged, lambda publisher, key: SECRET)
    with pytest.raises(PermissionError):
        verify_task(envelope, lambda publisher, key: None)
