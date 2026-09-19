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

TASK_VERSION = "ResearchTaskV1"
ENVELOPE_VERSION = "AuthenticatedEnvelopeV1"
AUTHENTICATION_METHOD = "HMAC-SHA256-V1"
MAX_TASK_BYTES = 32_768
MAX_ENVELOPE_BYTES = 65_536
MAX_REFS = 16
REQUEST_TYPES = {"BACKTEST_EXISTING_HYPOTHESIS"}
PRIORITY_HINTS = {"LOW", "NORMAL", "HIGH"}
REFERENCE_KINDS = {"protocol", "dataset", "baseline", "cost_model", "evidence"}
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_SHA256 = re.compile(r"[a-f0-9]{64}\Z")
_SOURCE_SHA = re.compile(r"(?:[a-f0-9]{40}|[a-f0-9]{64})\Z")
_SYMBOL = re.compile(r"[A-Z0-9]{3,20}\Z")


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


def payload_hash(payload) -> str:
    validate_task(payload)
    return digest(canonical(payload))


def _unsigned(envelope):
    return {key: value for key, value in envelope.items() if key != "signature"}


def sign_task(
    task,
    *,
    producer: str,
    publisher_identity: str,
    consumer: str,
    scope: str,
    key_id: str,
    secret: bytes,
):
    validate_task(task)
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
    task_hash = payload_hash(task)
    message_id = digest(canonical([TASK_VERSION, task["task_id"], task_hash]))
    envelope = {
        "schema_version": ENVELOPE_VERSION,
        "message_type": TASK_VERSION,
        "message_id": message_id,
        "producer": producer,
        "publisher_identity": publisher_identity,
        "consumer": consumer,
        "scope": scope,
        "created_at": task["created_at"],
        "payload_hash": task_hash,
        "payload": task,
        "key_id": key_id,
        "authentication_method": AUTHENTICATION_METHOD,
    }
    envelope["signature"] = hmac.new(secret, canonical(envelope), hashlib.sha256).hexdigest()
    return envelope


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
    if envelope["schema_version"] != ENVELOPE_VERSION or envelope["message_type"] != TASK_VERSION:
        raise ValueError("CONTRACT_INVALID: unsupported envelope")
    if envelope["authentication_method"] != AUTHENTICATION_METHOD:
        raise ValueError("CONTRACT_INVALID: unsupported authentication method")
    for field in ("producer", "publisher_identity", "consumer", "scope", "key_id"):
        _string(envelope[field], field, pattern=_ID)
    _string(envelope["message_id"], "message_id", pattern=_SHA256)
    _string(envelope["payload_hash"], "payload_hash", pattern=_SHA256)
    _string(envelope["signature"], "signature", pattern=_SHA256)
    _timestamp(envelope["created_at"], "envelope created_at")
    validate_task(envelope["payload"])
    expected_hash = payload_hash(envelope["payload"])
    if envelope["payload_hash"] != expected_hash:
        raise ValueError("CONTRACT_INVALID: payload hash mismatch")
    expected_id = digest(canonical([TASK_VERSION, envelope["payload"]["task_id"], expected_hash]))
    if envelope["message_id"] != expected_id:
        raise ValueError("CONTRACT_INVALID: message identity mismatch")
    if envelope["created_at"] != envelope["payload"]["created_at"]:
        raise ValueError("CONTRACT_INVALID: envelope/task time mismatch")
    if len(canonical(envelope)) > MAX_ENVELOPE_BYTES:
        raise ValueError("CONTRACT_INVALID: envelope exceeds size limit")
    return envelope


def verify_task(envelope, key_resolver: Callable[[str, str], bytes | None]):
    validate_envelope(envelope)
    secret = key_resolver(envelope["publisher_identity"], envelope["key_id"])
    if type(secret) is not bytes or len(secret) < 32:
        raise PermissionError("UNAUTHORIZED: unknown or revoked publisher key")
    expected = hmac.new(secret, canonical(_unsigned(envelope)), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(envelope["signature"], expected):
        raise PermissionError("UNAUTHORIZED: invalid publisher signature")
    return envelope


__all__ = [
    "AUTHENTICATION_METHOD",
    "ENVELOPE_VERSION",
    "TASK_VERSION",
    "canonical",
    "digest",
    "loads",
    "payload_hash",
    "sign_task",
    "validate_envelope",
    "validate_reference",
    "validate_task",
    "verify_task",
]
