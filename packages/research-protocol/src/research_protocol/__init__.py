"""Pure-stdlib contracts for authenticated, bounded research messages.

The package owns interchange syntax and cryptographic envelope verification. It
does not own admission policy, scheduling, execution, scientific interpretation,
economic interpretation, or capital authorization.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import unicodedata
from collections.abc import Callable
from datetime import datetime

from .key_store import HmacKeyStore

TASK_VERSION = "ResearchTaskV1"
RESULT_VERSION = "ResearchResultV1"
ENVELOPE_VERSION = "AuthenticatedEnvelopeV1"
AUTHENTICATION_METHOD = "HMAC-SHA256-V1"
MAX_TASK_BYTES = 32_768
MAX_RESULT_BYTES = 131_072
MAX_ENVELOPE_BYTES = 196_608
MAX_REFS = 16
REQUEST_TYPES = {"BACKTEST_EXISTING_HYPOTHESIS"}
PRIORITY_HINTS = {"LOW", "NORMAL", "HIGH"}
REFERENCE_KINDS = {"protocol", "dataset", "baseline", "cost_model", "evidence"}
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_SHA256 = re.compile(r"[a-f0-9]{64}\Z")
_SOURCE_SHA = re.compile(r"(?:[a-f0-9]{40}|[a-f0-9]{64})\Z")
_SYMBOL = re.compile(r"[A-Z0-9]{3,20}\Z")
OPERATIONAL_STATES = {
    "QUEUED",
    "RUNNING",
    "SUCCEEDED",
    "PARTIAL",
    "DEGRADED",
    "FAILED",
    "SKIPPED",
    "WAITING",
    "SOURCE_UNAVAILABLE",
    "CONFIGURATION_ERROR",
}
SCIENTIFIC_STATES = {
    "PROPOSED",
    "ACTIVE",
    "INCONCLUSIVE",
    "SUPPORTED",
    "REFUTED",
    "CLOSED_INSUFFICIENT_SAMPLE",
}
ECONOMIC_STATES = {"NO_EDGE", "WATCH", "PAPER_ELIGIBLE", "PAPER_ACTIVE", "PAPER_FAILED"}


def _normal(value):
    if value is None or type(value) in (bool, int):
        return value
    if type(value) is float:
        raise ValueError("CONTRACT_INVALID: floating-point values are forbidden")
    if type(value) is str:
        return unicodedata.normalize("NFC", value)
    if type(value) is list:
        return [_normal(item) for item in value]
    if type(value) is dict:
        normalized = {}
        for key, item in value.items():
            if type(key) is not str:
                raise ValueError("CONTRACT_INVALID: object keys must be strings")
            key = unicodedata.normalize("NFC", key)
            if key in normalized:
                raise ValueError("CONTRACT_INVALID: duplicate key after NFC normalization")
            normalized[key] = _normal(item)
        return normalized
    raise ValueError("CONTRACT_INVALID: unsupported JSON value")


def canonical(value) -> bytes:
    """UTF-8, NFC, sorted keys, explicit nulls, integers only, no whitespace."""
    return json.dumps(
        _normal(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def loads(value: bytes):
    def pairs(items):
        result = {}
        for key, item in items:
            if key in result:
                raise ValueError("CONTRACT_INVALID: duplicate JSON key")
            result[key] = item
        return result

    parsed = json.loads(value, object_pairs_hook=pairs, parse_float=lambda _: (_ for _ in ()).throw(
        ValueError("CONTRACT_INVALID: floating-point values are forbidden")
    ))
    if canonical(parsed) != value:
        raise ValueError("CONTRACT_INVALID: input is not canonical JSON")
    return parsed


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _keys(value, expected: set[str], label: str):
    if type(value) is not dict or set(value) != expected:
        raise ValueError(f"CONTRACT_INVALID: unexpected or missing {label} fields")


def _string(value, label: str, *, pattern=None, nullable=False, limit=500):
    if value is None and nullable:
        return
    if type(value) is not str or not value or len(value) > limit:
        raise ValueError(f"CONTRACT_INVALID: invalid {label}")
    if unicodedata.normalize("NFC", value) != value:
        raise ValueError(f"CONTRACT_INVALID: {label} must be NFC")
    if pattern is not None and pattern.fullmatch(value) is None:
        raise ValueError(f"CONTRACT_INVALID: invalid {label}")


def _timestamp(value, label: str) -> datetime:
    _string(value, label)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"CONTRACT_INVALID: invalid {label}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"CONTRACT_INVALID: {label} requires timezone")
    return parsed


def _integer(value, label: str, low: int, high: int):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"CONTRACT_INVALID: invalid {label}")


def validate_reference(reference, expected_kind: str | None = None):
    _keys(reference, {"kind", "name", "version"}, "reference")
    if reference["kind"] not in REFERENCE_KINDS:
        raise ValueError("CONTRACT_INVALID: unknown reference kind")
    if expected_kind is not None and reference["kind"] != expected_kind:
        raise ValueError("CONTRACT_INVALID: wrong reference kind")
    _string(reference["name"], "reference name", pattern=_NAME)
    _string(reference["version"], "reference version", pattern=_NAME)
    return reference


def _references(value, kind: str):
    if type(value) is not list or not 1 <= len(value) <= MAX_REFS:
        raise ValueError("CONTRACT_INVALID: invalid reference list")
    seen = set()
    for item in value:
        validate_reference(item, kind)
        identity = canonical(item)
        if identity in seen:
            raise ValueError("CONTRACT_INVALID: duplicate reference")
        seen.add(identity)


def validate_task(task):
    _keys(
        task,
        {
            "schema_version",
            "task_id",
            "research_id",
            "parent_task_id",
            "hypothesis_id",
            "domain",
            "request_type",
            "protocol_ref",
            "dataset_constraint_ref",
            "baseline_refs",
            "cost_model_ref",
            "evidence_refs",
            "bounded_parameters",
            "priority_hint",
            "created_at",
            "expires_at",
            "requested_by",
            "provenance",
        },
        "ResearchTaskV1",
    )
    if task["schema_version"] != TASK_VERSION or task["domain"] != "crypto":
        raise ValueError("CONTRACT_INVALID: unsupported task contract or domain")
    for field in ("task_id", "research_id", "hypothesis_id", "requested_by"):
        _string(task[field], field, pattern=_ID)
    _string(task["parent_task_id"], "parent_task_id", pattern=_ID, nullable=True)
    if task["parent_task_id"] == task["task_id"]:
        raise ValueError("CONTRACT_INVALID: task cannot parent itself")
    if task["request_type"] not in REQUEST_TYPES:
        raise ValueError("CONTRACT_INVALID: request type has no contract handler")
    validate_reference(task["protocol_ref"], "protocol")
    validate_reference(task["dataset_constraint_ref"], "dataset")
    _references(task["baseline_refs"], "baseline")
    validate_reference(task["cost_model_ref"], "cost_model")
    _references(task["evidence_refs"], "evidence")
    parameters = task["bounded_parameters"]
    _keys(
        parameters,
        {"symbol", "horizon_days", "max_observations", "fee_bps", "slippage_bps"},
        "BACKTEST_EXISTING_HYPOTHESIS parameters",
    )
    _string(parameters["symbol"], "symbol", pattern=_SYMBOL)
    _integer(parameters["horizon_days"], "horizon_days", 1, 365)
    _integer(parameters["max_observations"], "max_observations", 30, 100_000)
    _integer(parameters["fee_bps"], "fee_bps", 0, 1_000)
    _integer(parameters["slippage_bps"], "slippage_bps", 0, 1_000)
    if task["priority_hint"] not in PRIORITY_HINTS:
        raise ValueError("CONTRACT_INVALID: invalid priority_hint")
    created = _timestamp(task["created_at"], "created_at")
    expires = _timestamp(task["expires_at"], "expires_at")
    if expires <= created:
        raise ValueError("CONTRACT_INVALID: expires_at must follow created_at")
    provenance = task["provenance"]
    _keys(provenance, {"cain_source_sha", "retrieval_receipt_ids", "proposal_model"}, "provenance")
    _string(provenance["cain_source_sha"], "cain_source_sha", pattern=_SOURCE_SHA)
    _string(provenance["proposal_model"], "proposal_model", nullable=True, limit=200)
    receipts = provenance["retrieval_receipt_ids"]
    if type(receipts) is not list or len(receipts) > 50:
        raise ValueError("CONTRACT_INVALID: invalid retrieval receipts")
    for receipt in receipts:
        _string(receipt, "retrieval receipt", pattern=_ID)
    if len(receipts) != len(set(receipts)):
        raise ValueError("CONTRACT_INVALID: duplicate retrieval receipt")
    if len(canonical(task)) > MAX_TASK_BYTES:
        raise ValueError("CONTRACT_INVALID: task exceeds size limit")
    return task


def _identity(value, label):
    _keys(value, {"package_version", "source_sha", "artifact_sha256"}, label)
    _string(value["package_version"], f"{label} package_version", pattern=_NAME)
    _string(value["source_sha"], f"{label} source_sha", pattern=_SOURCE_SHA)
    _string(value["artifact_sha256"], f"{label} artifact_sha256", pattern=_SHA256)


def _ids(value, label, *, required=True):
    if type(value) is not list or len(value) > 100 or (required and not value):
        raise ValueError(f"CONTRACT_INVALID: invalid {label}")
    for item in value:
        _string(item, label, pattern=_ID)
    if len(value) != len(set(value)):
        raise ValueError(f"CONTRACT_INVALID: duplicate {label}")


def _content_identity(value, label):
    _keys(value, {"name", "version", "content_hash"}, label)
    _string(value["name"], f"{label} name", pattern=_NAME)
    _string(value["version"], f"{label} version", pattern=_NAME)
    _string(value["content_hash"], f"{label} content_hash", pattern=_SHA256)


def validate_result(result):
    _keys(
        result,
        {
            "schema_version",
            "result_id",
            "task_id",
            "admission_id",
            "research_id",
            "hypothesis_id",
            "experiment_id",
            "result_envelope_state",
            "envelope_failure_reason",
            "produced_at",
            "core_facts",
            "ops_facts",
            "crypto_facts",
            "provenance",
        },
        "ResearchResultV1",
    )
    if result["schema_version"] != RESULT_VERSION:
        raise ValueError("CONTRACT_INVALID: unsupported result contract")
    for field in (
        "result_id",
        "task_id",
        "admission_id",
        "research_id",
        "hypothesis_id",
        "experiment_id",
    ):
        _string(result[field], field, pattern=_ID)
    produced = _timestamp(result["produced_at"], "produced_at")
    if result["result_envelope_state"] not in {"PRODUCED", "FAILED"}:
        raise ValueError("CONTRACT_INVALID: invalid result_envelope_state")
    _string(result["envelope_failure_reason"], "envelope_failure_reason", nullable=True)
    if (result["result_envelope_state"] == "FAILED") != (
        result["envelope_failure_reason"] is not None
    ):
        raise ValueError("CONTRACT_INVALID: envelope failure reason mismatch")

    core = result["core_facts"]
    _keys(
        core,
        {"identity", "trial_ids", "scientific_state", "temporal_integrity", "statistics_receipt_hash"},
        "CORE facts",
    )
    _identity(core["identity"], "CORE identity")
    _ids(core["trial_ids"], "trial id", required=False)
    if core["scientific_state"] not in SCIENTIFIC_STATES:
        raise ValueError("CONTRACT_INVALID: invalid scientific_state")
    if core["temporal_integrity"] not in {"PASS", "FAIL", "NOT_APPLICABLE", "NOT_VERIFIED"}:
        raise ValueError("CONTRACT_INVALID: invalid temporal integrity")
    _string(
        core["statistics_receipt_hash"],
        "statistics_receipt_hash",
        pattern=_SHA256,
        nullable=True,
    )

    ops = result["ops_facts"]
    _keys(
        ops,
        {
            "identity",
            "ops_run_ids",
            "operational_state",
            "started_at",
            "finished_at",
            "exit_code",
            "runtime_provenance_hash",
        },
        "OPS facts",
    )
    _identity(ops["identity"], "OPS identity")
    _ids(ops["ops_run_ids"], "OPS run id")
    if ops["operational_state"] not in OPERATIONAL_STATES:
        raise ValueError("CONTRACT_INVALID: invalid operational_state")
    started = _timestamp(ops["started_at"], "started_at")
    finished = _timestamp(ops["finished_at"], "finished_at")
    if finished < started or produced < finished:
        raise ValueError("CONTRACT_INVALID: invalid result time ordering")
    if ops["exit_code"] is not None and type(ops["exit_code"]) is not int:
        raise ValueError("CONTRACT_INVALID: invalid exit_code")
    _string(ops["runtime_provenance_hash"], "runtime_provenance_hash", pattern=_SHA256)

    crypto = result["crypto_facts"]
    _keys(
        crypto,
        {
            "identity",
            "dataset_identity",
            "model_identity",
            "feature_set_identity",
            "data_cutoff",
            "metrics",
            "baseline_comparison",
            "costs",
            "economic_state",
            "artifacts",
        },
        "CRIPTO facts",
    )
    _identity(crypto["identity"], "CRIPTO identity")
    _content_identity(crypto["dataset_identity"], "dataset identity")
    _content_identity(crypto["model_identity"], "model identity")
    _content_identity(crypto["feature_set_identity"], "feature set identity")
    data_cutoff = _timestamp(crypto["data_cutoff"], "data_cutoff")
    if data_cutoff > started:
        raise ValueError("CONTRACT_INVALID: data cutoff is after execution start")
    metrics = crypto["metrics"]
    _keys(
        metrics,
        {
            "sample_size",
            "gross_return_bps",
            "net_return_bps",
            "max_drawdown_bps",
            "turnover_bps",
            "ci_low_bps",
            "ci_high_bps",
        },
        "metrics",
    )
    _integer(metrics["sample_size"], "sample_size", 0, 10_000_000)
    for field in ("gross_return_bps", "net_return_bps", "ci_low_bps", "ci_high_bps"):
        _integer(metrics[field], field, -10_000_000, 10_000_000)
    _integer(metrics["max_drawdown_bps"], "max_drawdown_bps", -10_000_000, 0)
    _integer(metrics["turnover_bps"], "turnover_bps", 0, 10_000_000)
    if metrics["ci_low_bps"] > metrics["ci_high_bps"]:
        raise ValueError("CONTRACT_INVALID: inverted confidence interval")
    comparison = crypto["baseline_comparison"]
    _keys(
        comparison,
        {"baseline_id", "outcome", "gross_delta_bps", "net_delta_bps"},
        "baseline comparison",
    )
    _string(comparison["baseline_id"], "baseline_id", pattern=_ID)
    if comparison["outcome"] not in {"BEATS", "LOSES", "TIES"}:
        raise ValueError("CONTRACT_INVALID: invalid baseline outcome")
    for field in ("gross_delta_bps", "net_delta_bps"):
        _integer(comparison[field], field, -10_000_000, 10_000_000)
    expected_outcome = (
        "BEATS" if comparison["net_delta_bps"] > 0 else "LOSES" if comparison["net_delta_bps"] < 0 else "TIES"
    )
    if comparison["outcome"] != expected_outcome:
        raise ValueError("CONTRACT_INVALID: baseline outcome contradicts net delta")
    costs = crypto["costs"]
    _keys(costs, {"fee_bps", "slippage_bps", "total_cost_bps"}, "costs")
    for field in costs:
        _integer(costs[field], field, 0, 1_000_000)
    if costs["total_cost_bps"] != costs["fee_bps"] + costs["slippage_bps"]:
        raise ValueError("CONTRACT_INVALID: total cost mismatch")
    if metrics["net_return_bps"] != metrics["gross_return_bps"] - costs["total_cost_bps"]:
        raise ValueError("CONTRACT_INVALID: net result does not include declared costs")
    if crypto["economic_state"] not in ECONOMIC_STATES:
        raise ValueError("CONTRACT_INVALID: invalid economic_state")
    if metrics["net_return_bps"] <= 0 and crypto["economic_state"] not in {"NO_EDGE", "PAPER_FAILED"}:
        raise ValueError("CONTRACT_INVALID: non-positive net result cannot be economically promoted")
    artifacts = crypto["artifacts"]
    if type(artifacts) is not list or len(artifacts) > 32:
        raise ValueError("CONTRACT_INVALID: invalid artifacts")
    artifact_ids = set()
    for artifact in artifacts:
        _keys(artifact, {"artifact_id", "role", "sha256", "media_type", "size"}, "artifact")
        _string(artifact["artifact_id"], "artifact_id", pattern=_ID)
        _string(artifact["role"], "artifact role", pattern=_NAME)
        _string(artifact["sha256"], "artifact sha256", pattern=_SHA256)
        _string(artifact["media_type"], "artifact media_type", limit=100)
        _integer(artifact["size"], "artifact size", 0, 1_000_000_000)
        if artifact["artifact_id"] in artifact_ids:
            raise ValueError("CONTRACT_INVALID: duplicate artifact")
        artifact_ids.add(artifact["artifact_id"])

    provenance = result["provenance"]
    _keys(
        provenance,
        {"task_payload_hash", "admission_policy_hash", "resolved_references_hash", "crypto_source_sha"},
        "result provenance",
    )
    for field in ("task_payload_hash", "admission_policy_hash", "resolved_references_hash"):
        _string(provenance[field], field, pattern=_SHA256)
    _string(provenance["crypto_source_sha"], "crypto_source_sha", pattern=_SOURCE_SHA)
    if ops["operational_state"] in {"FAILED", "SOURCE_UNAVAILABLE", "CONFIGURATION_ERROR"}:
        if core["scientific_state"] not in {"ACTIVE", "INCONCLUSIVE"}:
            raise ValueError("CONTRACT_INVALID: failed execution cannot promote scientific state")
        if crypto["economic_state"] != "NO_EDGE":
            raise ValueError("CONTRACT_INVALID: failed execution cannot promote economic state")
    if len(canonical(result)) > MAX_RESULT_BYTES:
        raise ValueError("CONTRACT_INVALID: result exceeds size limit")
    return result


def validate_payload(payload):
    if type(payload) is not dict:
        raise ValueError("CONTRACT_INVALID: payload must be an object")
    if payload.get("schema_version") == TASK_VERSION:
        return validate_task(payload)
    if payload.get("schema_version") == RESULT_VERSION:
        return validate_result(payload)
    raise ValueError("CONTRACT_INVALID: unsupported payload")


def payload_hash(payload) -> str:
    validate_payload(payload)
    return digest(canonical(payload))


def _unsigned(envelope):
    return {key: value for key, value in envelope.items() if key != "signature"}


def _sign(
    payload,
    *,
    producer: str,
    publisher_identity: str,
    consumer: str,
    scope: str,
    key_id: str,
    secret: bytes,
):
    validate_payload(payload)
    for label, value in {
        "producer": producer,
        "publisher_identity": publisher_identity,
        "consumer": consumer,
        "scope": scope,
        "key_id": key_id,
    }.items():
        _string(value, label, pattern=_ID)
    if type(secret) is not bytes or len(secret) < 32:
        raise ValueError("AUTHENTICATION_INVALID: HMAC key must contain at least 32 bytes")
    version = payload["schema_version"]
    logical_id = payload["task_id"] if version == TASK_VERSION else payload["result_id"]
    created_at = payload["created_at"] if version == TASK_VERSION else payload["produced_at"]
    value_hash = payload_hash(payload)
    message_id = digest(canonical([version, logical_id, value_hash]))
    envelope = {
        "schema_version": ENVELOPE_VERSION,
        "message_type": version,
        "message_id": message_id,
        "producer": producer,
        "publisher_identity": publisher_identity,
        "consumer": consumer,
        "scope": scope,
        "created_at": created_at,
        "payload_hash": value_hash,
        "payload": payload,
        "key_id": key_id,
        "authentication_method": AUTHENTICATION_METHOD,
    }
    envelope["signature"] = hmac.new(secret, canonical(envelope), hashlib.sha256).hexdigest()
    return envelope


def sign_task(task, **identity):
    validate_task(task)
    return _sign(task, **identity)


def sign_result(result, **identity):
    validate_result(result)
    return _sign(result, **identity)


def validate_envelope(envelope):
    _keys(
        envelope,
        {
            "schema_version",
            "message_type",
            "message_id",
            "producer",
            "publisher_identity",
            "consumer",
            "scope",
            "created_at",
            "payload_hash",
            "payload",
            "key_id",
            "authentication_method",
            "signature",
        },
        "authenticated envelope",
    )
    if envelope["schema_version"] != ENVELOPE_VERSION or envelope["message_type"] not in {
        TASK_VERSION,
        RESULT_VERSION,
    }:
        raise ValueError("CONTRACT_INVALID: unsupported envelope")
    if envelope["authentication_method"] != AUTHENTICATION_METHOD:
        raise ValueError("CONTRACT_INVALID: unsupported authentication method")
    for field in ("producer", "publisher_identity", "consumer", "scope", "key_id"):
        _string(envelope[field], field, pattern=_ID)
    _string(envelope["message_id"], "message_id", pattern=_SHA256)
    _string(envelope["payload_hash"], "payload_hash", pattern=_SHA256)
    _string(envelope["signature"], "signature", pattern=_SHA256)
    _timestamp(envelope["created_at"], "envelope created_at")
    validate_payload(envelope["payload"])
    if envelope["message_type"] != envelope["payload"]["schema_version"]:
        raise ValueError("CONTRACT_INVALID: envelope/payload type mismatch")
    expected_hash = payload_hash(envelope["payload"])
    if envelope["payload_hash"] != expected_hash:
        raise ValueError("CONTRACT_INVALID: payload hash mismatch")
    logical_id = (
        envelope["payload"]["task_id"]
        if envelope["message_type"] == TASK_VERSION
        else envelope["payload"]["result_id"]
    )
    expected_id = digest(canonical([envelope["message_type"], logical_id, expected_hash]))
    if envelope["message_id"] != expected_id:
        raise ValueError("CONTRACT_INVALID: message identity mismatch")
    payload_time = (
        envelope["payload"]["created_at"]
        if envelope["message_type"] == TASK_VERSION
        else envelope["payload"]["produced_at"]
    )
    if envelope["created_at"] != payload_time:
        raise ValueError("CONTRACT_INVALID: envelope/payload time mismatch")
    if len(canonical(envelope)) > MAX_ENVELOPE_BYTES:
        raise ValueError("CONTRACT_INVALID: envelope exceeds size limit")
    return envelope


def verify_task(envelope, key_resolver: Callable[[str, str], bytes | None]):
    validate_envelope(envelope)
    if envelope["message_type"] != TASK_VERSION:
        raise ValueError("CONTRACT_INVALID: expected ResearchTaskV1")
    return _verify(envelope, key_resolver)


def _verify(envelope, key_resolver):
    secret = key_resolver(envelope["publisher_identity"], envelope["key_id"])
    if type(secret) is not bytes or len(secret) < 32:
        raise PermissionError("UNAUTHORIZED: unknown or revoked publisher key")
    expected = hmac.new(secret, canonical(_unsigned(envelope)), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(envelope["signature"], expected):
        raise PermissionError("UNAUTHORIZED: invalid publisher signature")
    return envelope


def verify_result(envelope, key_resolver: Callable[[str, str], bytes | None]):
    validate_envelope(envelope)
    if envelope["message_type"] != RESULT_VERSION:
        raise ValueError("CONTRACT_INVALID: expected ResearchResultV1")
    return _verify(envelope, key_resolver)


__all__ = [
    "AUTHENTICATION_METHOD",
    "ENVELOPE_VERSION",
    "HmacKeyStore",
    "RESULT_VERSION",
    "TASK_VERSION",
    "canonical",
    "digest",
    "loads",
    "payload_hash",
    "sign_result",
    "sign_task",
    "validate_envelope",
    "validate_payload",
    "validate_reference",
    "validate_result",
    "validate_task",
    "verify_result",
    "verify_task",
]
