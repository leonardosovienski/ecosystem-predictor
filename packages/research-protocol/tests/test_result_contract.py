from copy import deepcopy

import pytest
from research_protocol import payload_hash, sign_result, validate_result, verify_result

SECRET = bytes.fromhex("22" * 32)
SHA256 = "ab" * 32
SOURCE_SHA = "12" * 20


def identity(name):
    del name
    return {"package_version": "1.0.0", "source_sha": SOURCE_SHA, "artifact_sha256": SHA256}


def content(name):
    return {"name": name, "version": "v1", "content_hash": SHA256}


def result():
    return {
        "schema_version": "ResearchResultV1",
        "result_id": "RESULT-001",
        "task_id": "TASK-001",
        "admission_id": "ADMISSION-001",
        "research_id": "RESEARCH-001",
        "hypothesis_id": "H6",
        "experiment_id": "EXPERIMENT-001",
        "result_envelope_state": "PRODUCED",
        "envelope_failure_reason": None,
        "produced_at": "2026-09-19T23:03:00Z",
        "core_facts": {
            "identity": identity("predictor-core"),
            "trial_ids": ["TRIAL-001"],
            "scientific_state": "REFUTED",
            "temporal_integrity": "PASS",
            "statistics_receipt_hash": SHA256,
        },
        "ops_facts": {
            "identity": identity("predictor-ops"),
            "ops_run_ids": ["OPS-RUN-001"],
            "operational_state": "SUCCEEDED",
            "started_at": "2026-09-19T23:00:00Z",
            "finished_at": "2026-09-19T23:02:00Z",
            "exit_code": 0,
            "runtime_provenance_hash": SHA256,
        },
        "crypto_facts": {
            "identity": identity("crypto-predictor"),
            "dataset_identity": content("btc-daily-pit"),
            "model_identity": content("deterministic-baseline"),
            "feature_set_identity": content("features-v1"),
            "data_cutoff": "2026-09-18T00:00:00Z",
            "metrics": {
                "sample_size": 500,
                "gross_return_bps": 30,
                "net_return_bps": -20,
                "max_drawdown_bps": -120,
                "turnover_bps": 400,
                "ci_low_bps": -100,
                "ci_high_bps": 50,
            },
            "baseline_comparison": {
                "baseline_id": "BASELINE-001",
                "outcome": "LOSES",
                "gross_delta_bps": 10,
                "net_delta_bps": -10,
            },
            "costs": {"fee_bps": 20, "slippage_bps": 30, "total_cost_bps": 50},
            "economic_state": "NO_EDGE",
            "artifacts": [
                {
                    "artifact_id": "ARTIFACT-001",
                    "role": "metrics",
                    "sha256": SHA256,
                    "media_type": "application/json",
                    "size": 512,
                }
            ],
        },
        "provenance": {
            "task_payload_hash": SHA256,
            "admission_policy_hash": SHA256,
            "resolved_references_hash": SHA256,
            "crypto_source_sha": SOURCE_SHA,
        },
    }


def signed(value=None):
    return sign_result(
        value or result(),
        producer="CRIPTO",
        publisher_identity="crypto-qa",
        consumer="CAIN",
        scope="crypto.research.result",
        key_id="crypto-f4-key",
        secret=SECRET,
    )


def test_result_roundtrip_preserves_separate_authorities_and_states():
    value = result()
    assert value["ops_facts"]["operational_state"] == "SUCCEEDED"
    assert value["core_facts"]["scientific_state"] == "REFUTED"
    assert value["crypto_facts"]["economic_state"] == "NO_EDGE"
    envelope = signed(value)
    assert verify_result(envelope, lambda publisher, key: SECRET) == envelope
    assert envelope["payload_hash"] == payload_hash(value)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["crypto_facts"]["costs"].update(total_cost_bps=49),
        lambda value: value["crypto_facts"].update(economic_state="PAPER_ELIGIBLE"),
        lambda value: value["crypto_facts"]["baseline_comparison"].update(outcome="BEATS"),
        lambda value: value["core_facts"].update(owner="CRIPTO"),
        lambda value: value["ops_facts"].update(started_at="2026-09-20T00:00:00Z"),
        lambda value: value["crypto_facts"].update(data_cutoff="2026-09-20T00:00:00Z"),
        lambda value: value["crypto_facts"]["metrics"].update(turnover_bps=-1),
    ],
)
def test_result_fails_closed_on_contradictions_or_unknown_fields(mutation):
    value = result()
    mutation(value)
    with pytest.raises(ValueError):
        validate_result(value)


def test_failed_execution_cannot_claim_scientific_or_economic_promotion():
    value = result()
    value["ops_facts"]["operational_state"] = "FAILED"
    value["core_facts"]["scientific_state"] = "SUPPORTED"
    with pytest.raises(ValueError):
        validate_result(value)


def test_forged_or_unknown_result_publisher_fails_closed():
    envelope = signed()
    forged = deepcopy(envelope)
    forged["signature"] = "00" * 32
    with pytest.raises(PermissionError):
        verify_result(forged, lambda publisher, key: SECRET)
    with pytest.raises(PermissionError):
        verify_result(envelope, lambda publisher, key: None)
