"""Vectors for the V2 envelope tests: one valid request per domain contract and domain results."""

from __future__ import annotations

import copy


def _ref(name: str) -> dict:
    return {"name": name, "version": "v1"}


REQUESTS = {
    "crypto": {
        "schema_version": "crypto-research-request/1",
        "request_id": "crypto:REQ-0001",
        "request_type": "BACKTEST_EXISTING_HYPOTHESIS",
        "research_id": "crypto:RESEARCH-0001",
        "hypothesis_id": "crypto:QUAL-H1",
        "references": {
            "protocol": _ref("protocol-std"),
            "dataset": _ref("dataset-btc"),
            "baseline": _ref("baseline-hold"),
            "cost_model": _ref("costs-std"),
            "evidence": _ref("evidence-none"),
        },
        "data_cutoff": "2026-08-31T00:00:00Z",
        "parameters": {
            "symbol": "BTCUSDT",
            "horizon_days": 7,
            "max_observations": 200,
            "fee_bps": 10,
            "slippage_bps": 5,
        },
        "priority_hint": "NORMAL",
    },
    "stocks": {
        "schema_version": "stocks-research-request/1",
        "request_id": "stocks:REQ-0001",
        "request_type": "BACKTEST_PIT_FACTOR",
        "research_id": "stocks:RESEARCH-0001",
        "hypothesis_id": "stocks:QUAL-PIT-MOM-001",
        "references": {
            "dataset": _ref("panel"),
            "universe": _ref("universe-top100"),
            "features": _ref("features-mom"),
            "model": _ref("model-rank"),
            "baseline": _ref("baseline-ew"),
            "cost_model": _ref("costs-b3"),
            "readiness": _ref("readiness"),
        },
        "as_of": "2026-09-24T03:00:00Z",
        "pit": {
            "availability_rule": "AVAILABLE_AT_LE_DECISION_TIME",
            "minimum_pit_class": "PIT_RECONSTRUCTED",
        },
        "parameters": {
            "target": "NEXT_REBALANCE_RETURN",
            "fee_bps": 10,
            "slippage_bps": 5,
            "max_securities": 50,
            "external_intelligence": {"mode": "NONE", "families": []},
        },
        "priority_hint": "NORMAL",
    },
    "brasileirao": {
        "schema_version": "brasileirao-research-request/1",
        "request_id": "brasileirao:REQ-0001",
        "request_type": "WALKFORWARD_FORECAST_EVALUATION",
        "research_id": "brasileirao:RESEARCH-0001",
        "hypothesis_id": "brasileirao:QUAL-H1",
        "competition": "Brasileirão Série A",
        "season": 2024,
        "target": "1X2",
        "events": {"kickoff_from": "2024-04-01T00:00:00Z", "kickoff_to": "2024-12-31T00:00:00Z"},
        "data_cutoff": "2024-04-01T00:00:00Z",
        "decision_lead_minutes": 60,
        "references": {
            "dataset": _ref("matches"),
            "model": _ref("dixon-coles"),
            "features": _ref("features"),
            "baseline": _ref("climatology"),
            "cost_model": _ref("costs"),
        },
        "priority_hint": "NORMAL",
    },
}

_COMMON_RESULT_FIELDS = (
    "schema_version",
    "result_id",
    "request_id",
    "admission_id",
    "experiment_id",
    "research_id",
    "hypothesis_id",
    "result_state",
    "operational_state",
    "scientific_state",
    "economic_state",
    "capital_permission",
    "produced_at",
    "core_facts",
    "ops_facts",
    "domain_facts",
    "provenance",
)


def domain_result(domain: str, request: dict) -> dict:
    """A result shaped like the domain contract (floats included, as real results have)."""
    result = {
        "schema_version": f"{domain}-research-result/1",
        "result_id": f"{domain}:RESULT-" + "a" * 32,
        "request_id": request["request_id"],
        "admission_id": f"{domain}:ADM-" + "b" * 32,
        "experiment_id": f"{domain}:EXP-" + "c" * 32,
        "research_id": request["research_id"],
        "hypothesis_id": request["hypothesis_id"],
        "result_state": "NO_EDGE",
        "operational_state": "SUCCEEDED",
        "scientific_state": "INCONCLUSIVE",
        "economic_state": "NO_EDGE",
        "capital_permission": False,
        "produced_at": "2026-09-24T10:00:00Z",
        "core_facts": {"trial_ids": [f"{domain}:TRIAL-" + "d" * 32], "ci": [-0.25, 0.125]},
        "ops_facts": {"ops_run_id": "run-1", "retry_count": 0},
        "domain_facts": {"metric": 0.1 + 0.2, "texto": "ção"},
        "provenance": {"admission_policy_hash": "e" * 64},
    }
    if domain == "stocks":
        result.update(
            {"as_of": request["as_of"], "request_type": request["request_type"], "trial_eligible": False}
        )
    return result


def outcome(domain: str, task: dict, status: str = "RESULT") -> dict:
    """A domain outcome as Circuit.submit_request returns it."""
    request = task["payload"]
    out = {
        "schema": f"{domain}-research-outcome/1",
        "submission_file": "adapter:" + task["task_id"],
        "submission_sha256": "f" * 64,
        "at": "2026-09-24T10:00:01Z",
        "request_id": request["request_id"],
        "client_ref": copy.deepcopy(request["client_ref"]),
        "status": status,
    }
    if status in ("RESULT", "DUPLICATE"):
        result = domain_result(domain, request)
        out.update(
            {
                "result_id": result["result_id"],
                "experiment_id": result["experiment_id"],
                "result_state": result["result_state"],
                "operational_state": result["operational_state"],
                "scientific_state": result["scientific_state"],
                "economic_state": result["economic_state"],
                "capital_permission": False,
                "result": result,
            }
        )
    else:
        out["reason"] = "HYPOTHESIS_NOT_ADMITTED" if status == "REJECTED" else "X"
    out["exit_code"] = {
        "RESULT": 0,
        "DUPLICATE": 0,
        "REJECTED": 2,
        "CONFLICT": 2,
        "NOT_READY": 3,
        "OPS_FAILED_RETRYABLE": 3,
        "TEMPORAL_INTEGRITY_VIOLATION": 4,
        "RECONCILIATION_REQUIRED": 5,
        "STATE_BUSY_RETRYABLE": 3,
        "STORAGE_FAILED_RETRYABLE": 3,
    }[status]
    return out


ADAPTER = {"distribution": "test-domain", "version": "0.0.0", "module": "tests.adapter"}
