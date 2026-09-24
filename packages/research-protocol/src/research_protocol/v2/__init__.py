"""ResearchTaskV2 / ResearchResultV2: the domain-neutral envelope of the Stage B integration.

Specification: ``packages/research-protocol/SPEC_V2.md``. Pure stdlib, no I/O besides reading the
packaged domain registry. The envelope owns syntax, correlation and fail-closed rejection only:
it never chooses a handler, a budget, a priority or capital, and it never interprets the
operational, scientific or economic states it carries.

* Task payload = the domain request (``request_schema`` of the contract, by ``domain_prefix``),
  validated against the schema copied verbatim from the contract. The envelope owns ``client_ref``.
* Result payload = the exact canonical bytes of the domain result (``result_schema``), carried as
  a string so that floats inside the domain result never pass through a second serialization.
* Serialization is canonical JSON (sorted keys, no whitespace, UTF-8, no NaN/Infinity); a
  non-canonical input, an unknown field, an unknown version or an ambiguous ID is rejected.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from importlib.resources import files
from types import MappingProxyType
from typing import Any

from ._schema import InstanceError, SchemaError, check_schema, validate

TASK_SCHEMA = "research-task/2"
RESULT_SCHEMA = "research-result/2"
CLIENT_REF_SCHEMA = "research-client-ref/2"
PRODUCERS = ("cain",)
MAX_REQUEST_BYTES = 256 * 1024
MAX_TASK_BYTES = 320 * 1024
MAX_RESULT_BYTES = 32 * 1024 * 1024
MAX_BASED_ON = 64
MAX_REASON_CHARS = 300

# How a consumer may treat each domain outcome status (the domain decides the status).
OUTCOME_CLASSES = MappingProxyType(
    {
        "RESULT": "TERMINAL_RESULT",
        "DUPLICATE": "TERMINAL_RESULT",
        "REJECTED": "TERMINAL_REFUSAL",
        "CONFLICT": "TERMINAL_REFUSAL",
        "TEMPORAL_INTEGRITY_VIOLATION": "TERMINAL_REFUSAL",
        "NOT_READY": "RETRYABLE",
        "OPS_FAILED_RETRYABLE": "RETRYABLE",
        "STATE_BUSY_RETRYABLE": "RETRYABLE",
        "STORAGE_FAILED_RETRYABLE": "RETRYABLE",
        "RECONCILIATION_REQUIRED": "REQUIRES_HUMAN",
    }
)
RESULT_STATUSES = frozenset({"RESULT", "DUPLICATE"})

TASK_FIELDS = frozenset(
    {
        "based_on",
        "created_at",
        "domain",
        "hypothesis_id",
        "payload",
        "payload_schema",
        "payload_sha256",
        "producer",
        "proposal_id",
        "request_id",
        "research_id",
        "schema",
        "task_id",
    }
)
RESULT_FIELDS = frozenset(
    {
        "adapter",
        "client_ref",
        "domain",
        "hypothesis_id",
        "outcome",
        "produced_at",
        "request_id",
        "research_id",
        "result",
        "schema",
        "task_id",
    }
)
OUTCOME_FIELDS = frozenset({"exit_code", "reason", "status"})
RESULT_BODY_FIELDS = frozenset(
    {
        "admission_id",
        "capital_permission",
        "economic_state",
        "experiment_id",
        "operational_state",
        "payload_canonical",
        "payload_schema",
        "payload_sha256",
        "result_id",
        "result_state",
        "scientific_state",
    }
)
ADAPTER_FIELDS = frozenset({"distribution", "module", "version"})
_ID_TAIL = r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}"
_UTC = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_CAIN_ID = re.compile(r"cain:" + _ID_TAIL + r"\Z")
_TEXT = re.compile(r"[\x20-\x7e]{1,200}\Z")


class V2Error(ValueError):
    """Fail-closed rejection with a stable reason code."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def _load_registry() -> dict[str, Any]:
    raw = files("research_protocol.v2").joinpath("data/domains.json").read_bytes()
    registry = json.loads(raw)
    if registry.get("schema") != "research-protocol-v2-domains/1":
        raise SchemaError("unknown domain registry schema")
    for name, entry in registry["domains"].items():
        check_schema(entry["request_schema"], path=f"domains/{name}/request_schema")
        if entry["request_schema"].get("$id") != entry["request_schema_id"]:
            raise SchemaError(f"domains/{name}: request_schema $id mismatch")
    return registry


REGISTRY = _load_registry()
REGISTRY_SHA256 = hashlib.sha256(
    files("research_protocol.v2").joinpath("data/domains.json").read_bytes()
).hexdigest()
DOMAINS = tuple(sorted(REGISTRY["domains"]))


# --------------------------------------------------------------------------- serialization
def _reject_floats(value: Any, path: str = "$") -> None:
    if type(value) is float:
        raise V2Error("FLOAT_FORBIDDEN", f"floating-point value at {path}")
    if isinstance(value, dict):
        for key, item in value.items():
            if type(key) is not str:
                raise V2Error("SCHEMA_INVALID", f"non-string key at {path}")
            _reject_floats(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_floats(item, f"{path}[{index}]")
    elif value is not None and type(value) not in (bool, int, str):
        raise V2Error("SCHEMA_INVALID", f"unsupported JSON value at {path}")


def domain_canonical(value: Any) -> bytes:
    """The domains' canonical JSON (identical to their ``research_contract.canonical``)."""
    try:
        return json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise V2Error("SCHEMA_INVALID", f"not serializable as canonical JSON: {exc}") from exc


def canonical(value: Any) -> bytes:
    """Envelope canonical JSON: the domain canonical form, with floats forbidden."""
    _reject_floats(value)
    return domain_canonical(value)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def loads_strict(raw: bytes) -> Any:
    """Parse UTF-8 JSON rejecting duplicate keys and NaN/Infinity (floats are parsed)."""

    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise V2Error("SCHEMA_INVALID", f"duplicate key {key!r}")
            out[key] = value
        return out

    def constant(name):
        raise V2Error("SCHEMA_INVALID", f"non-finite constant {name}")

    if not isinstance(raw, (bytes, bytearray)):
        raise V2Error("SCHEMA_INVALID", "expected bytes")
    try:
        text = bytes(raw).decode("utf-8")
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except UnicodeDecodeError as exc:
        raise V2Error("SCHEMA_INVALID", "not UTF-8") from exc
    except json.JSONDecodeError as exc:
        raise V2Error("SCHEMA_INVALID", "invalid JSON") from exc


# --------------------------------------------------------------------------- helpers
def _domain(name: Any) -> dict[str, Any]:
    if type(name) is not str or name not in REGISTRY["domains"]:
        raise V2Error("DOMAIN_UNKNOWN", f"unknown domain {name!r}")
    return REGISTRY["domains"][name]


def _qualified(value: Any, domain: str, field: str) -> str:
    if type(value) is not str:
        raise V2Error("ID_NOT_QUALIFIED", f"{field} must be a string")
    if not re.fullmatch(re.escape(domain) + ":" + _ID_TAIL, value):
        prefix = value.split(":", 1)[0] if ":" in value else None
        code = "DOMAIN_MISMATCH" if prefix in REGISTRY["domains"] and prefix != domain else "ID_NOT_QUALIFIED"
        raise V2Error(code, f"{field} {value[:140]!r} is not a {domain}: qualified ID")
    return value


def _utc(value: Any, field: str) -> str:
    if type(value) is not str or not _UTC.match(value):
        raise V2Error("SCHEMA_INVALID", f"{field} must be UTC 'YYYY-MM-DDTHH:MM:SSZ'")
    return value


def _exact_keys(value: Any, fields: frozenset[str], label: str) -> dict:
    if not isinstance(value, dict):
        raise V2Error("SCHEMA_INVALID", f"{label} must be an object")
    unknown = set(value) - fields
    if unknown:
        raise V2Error("UNKNOWN_FIELD", f"{label}: unknown fields {sorted(unknown)}")
    missing = fields - set(value)
    if missing:
        raise V2Error("SCHEMA_INVALID", f"{label}: missing fields {sorted(missing)}")
    return value


def request_content_hash(payload: dict) -> str:
    """sha256 of the canonical domain request without ``client_ref`` (the domains' content hash)."""
    return digest(canonical({key: value for key, value in payload.items() if key != "client_ref"}))


def task_id_for(domain: str, request_id: str, payload_sha256: str) -> str:
    material = canonical({"domain": domain, "payload_sha256": payload_sha256, "request_id": request_id})
    return f"{domain}:TASK-{digest(material)[:32]}"


def client_ref_for(task_id: str) -> dict:
    return {"schema": CLIENT_REF_SCHEMA, "task_id": task_id}


# --------------------------------------------------------------------------- task
def build_task(
    domain: str,
    request: dict,
    *,
    proposal_id: str,
    created_at: str,
    based_on: list[str] | tuple[str, ...] = (),
) -> dict:
    """Wrap a domain request (without ``client_ref``) in a ResearchTaskV2."""
    entry = _domain(domain)
    if not isinstance(request, dict):
        raise V2Error("PAYLOAD_INVALID", "request must be an object")
    if "client_ref" in request:
        raise V2Error("CLIENT_REF_RESERVED", "client_ref is owned by the V2 envelope")
    payload = copy.deepcopy(request)
    request_id = _qualified(payload.get("request_id"), domain, "payload.request_id")
    payload_sha256 = request_content_hash(payload)
    task_id = task_id_for(domain, request_id, payload_sha256)
    payload["client_ref"] = client_ref_for(task_id)
    task = {
        "schema": TASK_SCHEMA,
        "domain": domain,
        "task_id": task_id,
        "proposal_id": proposal_id,
        "based_on": list(based_on),
        "request_id": request_id,
        "research_id": payload.get("research_id"),
        "hypothesis_id": payload.get("hypothesis_id"),
        "created_at": created_at,
        "producer": "cain",
        "payload_schema": entry["request_schema_id"],
        "payload": payload,
        "payload_sha256": payload_sha256,
    }
    return validate_task(task)


def validate_task(task: Any) -> dict:
    if not isinstance(task, dict):
        raise V2Error("SCHEMA_INVALID", "task must be an object")
    if task.get("schema") != TASK_SCHEMA:
        raise V2Error("VERSION_UNSUPPORTED", f"task schema {str(task.get('schema'))[:60]!r}")
    _exact_keys(task, TASK_FIELDS, "task")
    domain = task["domain"]
    entry = _domain(domain)
    raw = canonical(task)
    if len(raw) > MAX_TASK_BYTES:
        raise V2Error("SIZE_LIMIT", "task larger than MAX_TASK_BYTES")
    if task["producer"] not in PRODUCERS:
        raise V2Error("SCHEMA_INVALID", "unknown producer")
    if type(task["proposal_id"]) is not str or not _CAIN_ID.match(task["proposal_id"]):
        raise V2Error("ID_NOT_QUALIFIED", "proposal_id must be a cain: qualified ID")
    _utc(task["created_at"], "created_at")
    based_on = task["based_on"]
    if not isinstance(based_on, list) or len(based_on) > MAX_BASED_ON:
        raise V2Error("SCHEMA_INVALID", "based_on must be a list of at most 64 IDs")
    for index, item in enumerate(based_on):
        _qualified(item, domain, f"based_on[{index}]")
    if len(set(based_on)) != len(based_on):
        raise V2Error("SCHEMA_INVALID", "based_on has duplicates")
    for field in ("request_id", "research_id", "hypothesis_id"):
        _qualified(task[field], domain, field)
    if task["payload_schema"] != entry["request_schema_id"]:
        raise V2Error("PAYLOAD_SCHEMA_MISMATCH", f"payload_schema must be {entry['request_schema_id']}")
    payload = task["payload"]
    if not isinstance(payload, dict):
        raise V2Error("PAYLOAD_INVALID", "payload must be an object")
    try:
        validate(payload, entry["request_schema"])
    except InstanceError as exc:
        raise V2Error("PAYLOAD_INVALID", str(exc)) from exc
    if len(canonical(payload)) > MAX_REQUEST_BYTES:
        raise V2Error("SIZE_LIMIT", "domain request larger than MAX_REQUEST_BYTES")
    for field in ("request_id", "research_id", "hypothesis_id"):
        if payload[field] != task[field]:
            raise V2Error("CORRELATION_MISMATCH", f"{field} differs between envelope and payload")
    if payload.get("client_ref") != client_ref_for(task["task_id"]):
        raise V2Error("CLIENT_REF_MISMATCH", "payload.client_ref must be the envelope client_ref")
    if type(task["payload_sha256"]) is not str or not _SHA256.match(task["payload_sha256"]):
        raise V2Error("SCHEMA_INVALID", "payload_sha256 must be lowercase sha256 hex")
    if request_content_hash(payload) != task["payload_sha256"]:
        raise V2Error("PAYLOAD_HASH_MISMATCH", "payload_sha256 does not match the payload")
    if task["task_id"] != task_id_for(domain, task["request_id"], task["payload_sha256"]):
        raise V2Error("TASK_ID_MISMATCH", "task_id is not derived from (domain, request_id, payload_sha256)")
    return task


def dumps_task(task: dict) -> bytes:
    return canonical(validate_task(task))


def loads_task(raw: bytes) -> dict:
    if isinstance(raw, (bytes, bytearray)) and len(raw) > MAX_TASK_BYTES:
        raise V2Error("SIZE_LIMIT", "task larger than MAX_TASK_BYTES")
    task = loads_strict(raw)
    if canonical(task) != bytes(raw):
        raise V2Error("NON_CANONICAL", "task bytes are not canonical JSON")
    return validate_task(task)


def request_bytes(task: dict) -> bytes:
    """The exact bytes the domain adapter submits through the adapter_api."""
    return canonical(validate_task(task)["payload"])


# --------------------------------------------------------------------------- result
def _check_domain_result(parsed: Any, entry: dict, domain: str) -> dict:
    if not isinstance(parsed, dict):
        raise V2Error("PAYLOAD_INVALID", "domain result must be an object")
    fields = set(entry["result_required_fields"])
    if set(parsed) != fields:
        raise V2Error(
            "PAYLOAD_INVALID",
            f"domain result fields differ from the contract: +{sorted(set(parsed) - fields)}"
            f" -{sorted(fields - set(parsed))}",
        )
    if parsed["schema_version"] != entry["result_schema_id"]:
        raise V2Error("PAYLOAD_SCHEMA_MISMATCH", "domain result schema_version")
    if parsed["capital_permission"] is not False:
        raise V2Error("CAPITAL_FORBIDDEN", "domain result grants capital")
    for field, allowed in (
        ("result_state", entry["result_states"]),
        ("operational_state", entry["operational_states"]),
        ("scientific_state", entry["scientific_states"]),
        ("economic_state", entry["economic_states"]),
    ):
        if parsed[field] not in allowed:
            raise V2Error("PAYLOAD_INVALID", f"domain result {field} {parsed[field]!r} not in contract")
    for field in ("result_id", "experiment_id", "admission_id", "request_id", "research_id", "hypothesis_id"):
        _qualified(parsed[field], domain, f"payload.{field}")
    return parsed


def build_result(task: dict, outcome: dict, *, adapter: dict, produced_at: str) -> dict:
    """Wrap one domain outcome (``Circuit.submit_request`` / ``show``) in a ResearchResultV2."""
    validate_task(task)
    domain = task["domain"]
    entry = _domain(domain)
    if not isinstance(outcome, dict):
        raise V2Error("OUTCOME_INVALID", "outcome must be an object")
    status = outcome.get("status")
    if status not in entry["outcome_exit_codes"]:
        raise V2Error("OUTCOME_INVALID", f"status {str(status)[:40]!r} not declared by {domain}")
    if outcome.get("exit_code", entry["outcome_exit_codes"][status]) != entry["outcome_exit_codes"][status]:
        raise V2Error("OUTCOME_INVALID", "exit_code does not match the status")
    if outcome.get("request_id") not in (None, task["request_id"]):
        raise V2Error("CORRELATION_MISMATCH", "outcome request_id differs from the task")
    reason = outcome.get("reason")
    body = None
    if status in RESULT_STATUSES:
        domain_result = outcome.get("result")
        raw = domain_canonical(domain_result)
        parsed = _check_domain_result(loads_strict(raw), entry, domain)
        for field in (
            "result_id",
            "experiment_id",
            "result_state",
            "operational_state",
            "scientific_state",
            "economic_state",
        ):
            if field in outcome and outcome[field] != parsed[field]:
                raise V2Error("CORRELATION_MISMATCH", f"outcome {field} differs from its result")
        body = {
            "result_id": parsed["result_id"],
            "experiment_id": parsed["experiment_id"],
            "admission_id": parsed["admission_id"],
            "result_state": parsed["result_state"],
            "operational_state": parsed["operational_state"],
            "scientific_state": parsed["scientific_state"],
            "economic_state": parsed["economic_state"],
            "capital_permission": False,
            "payload_schema": entry["result_schema_id"],
            "payload_sha256": digest(raw),
            "payload_canonical": raw.decode("utf-8"),
        }
    elif "result" in outcome:
        raise V2Error("OUTCOME_INVALID", f"status {status} must not carry a result")
    result = {
        "schema": RESULT_SCHEMA,
        "domain": domain,
        "task_id": task["task_id"],
        "request_id": task["request_id"],
        "research_id": task["research_id"],
        "hypothesis_id": task["hypothesis_id"],
        "outcome": {
            "status": status,
            "exit_code": entry["outcome_exit_codes"][status],
            "reason": None if reason is None else str(reason)[:MAX_REASON_CHARS],
        },
        "client_ref": outcome.get("client_ref"),
        "result": body,
        "produced_at": produced_at,
        "adapter": adapter,
    }
    return validate_result(result, task=task)


def validate_result(result: Any, *, task: dict | None = None) -> dict:
    if not isinstance(result, dict):
        raise V2Error("SCHEMA_INVALID", "result must be an object")
    if result.get("schema") != RESULT_SCHEMA:
        raise V2Error("VERSION_UNSUPPORTED", f"result schema {str(result.get('schema'))[:60]!r}")
    _exact_keys(result, RESULT_FIELDS, "result")
    domain = result["domain"]
    entry = _domain(domain)
    raw = canonical(result)
    if len(raw) > MAX_RESULT_BYTES:
        raise V2Error("SIZE_LIMIT", "result larger than MAX_RESULT_BYTES")
    if type(result["task_id"]) is not str or not re.fullmatch(
        re.escape(domain) + r":TASK-[0-9a-f]{32}", result["task_id"]
    ):
        _qualified(result["task_id"], domain, "task_id")
        raise V2Error("ID_NOT_QUALIFIED", "task_id must be <domain>:TASK-<32 hex>")
    for field in ("request_id", "research_id", "hypothesis_id"):
        _qualified(result[field], domain, field)
    _utc(result["produced_at"], "produced_at")
    adapter = _exact_keys(result["adapter"], ADAPTER_FIELDS, "adapter")
    for field in ADAPTER_FIELDS:
        if type(adapter[field]) is not str or not _TEXT.match(adapter[field]):
            raise V2Error("SCHEMA_INVALID", f"adapter.{field} must be printable ASCII")
    outcome = _exact_keys(result["outcome"], OUTCOME_FIELDS, "outcome")
    status = outcome["status"]
    if status not in entry["outcome_exit_codes"]:
        raise V2Error("OUTCOME_INVALID", f"status {str(status)[:40]!r} not declared by {domain}")
    if outcome["exit_code"] != entry["outcome_exit_codes"][status] or type(outcome["exit_code"]) is not int:
        raise V2Error("OUTCOME_INVALID", "exit_code does not match the status")
    if outcome["reason"] is not None and (
        type(outcome["reason"]) is not str or len(outcome["reason"]) > MAX_REASON_CHARS
    ):
        raise V2Error("SCHEMA_INVALID", "reason must be null or a string of at most 300 chars")
    expected_ref = client_ref_for(result["task_id"])
    if result["client_ref"] is None:
        if status != "REJECTED":
            raise V2Error(
                "CLIENT_REF_MISMATCH", "client_ref may be absent only when the request was rejected"
            )
    elif result["client_ref"] != expected_ref:
        raise V2Error("CLIENT_REF_MISMATCH", "client_ref does not echo the task")
    body = result["result"]
    if status in RESULT_STATUSES:
        _exact_keys(body, RESULT_BODY_FIELDS, "result.result")
        if body["payload_schema"] != entry["result_schema_id"]:
            raise V2Error("PAYLOAD_SCHEMA_MISMATCH", f"payload_schema must be {entry['result_schema_id']}")
        if body["capital_permission"] is not False:
            raise V2Error("CAPITAL_FORBIDDEN", "result grants capital")
        text = body["payload_canonical"]
        if type(text) is not str:
            raise V2Error("SCHEMA_INVALID", "payload_canonical must be a string")
        payload_raw = text.encode("utf-8")
        if type(body["payload_sha256"]) is not str or digest(payload_raw) != body["payload_sha256"]:
            raise V2Error("PAYLOAD_HASH_MISMATCH", "payload_sha256 does not match payload_canonical")
        parsed = loads_strict(payload_raw)
        if domain_canonical(parsed) != payload_raw:
            raise V2Error("NON_CANONICAL", "payload_canonical is not the domain canonical form")
        _check_domain_result(parsed, entry, domain)
        for field in (
            "result_id",
            "experiment_id",
            "admission_id",
            "result_state",
            "operational_state",
            "scientific_state",
            "economic_state",
        ):
            if body[field] != parsed[field]:
                raise V2Error("CORRELATION_MISMATCH", f"result.{field} differs from the domain payload")
        for field in ("request_id", "research_id", "hypothesis_id"):
            if parsed[field] != result[field]:
                raise V2Error("CORRELATION_MISMATCH", f"{field} differs from the domain payload")
    elif body is not None:
        raise V2Error("OUTCOME_INVALID", f"status {status} must not carry a result")
    if task is not None:
        validate_task(task)
        if task["domain"] != domain:
            raise V2Error("DOMAIN_MISMATCH", f"{domain} result offered for a {task['domain']} task")
        if task["task_id"] != result["task_id"]:
            raise V2Error("TASK_MISMATCH", "result belongs to another task")
        for field in ("request_id", "research_id", "hypothesis_id"):
            if task[field] != result[field]:
                raise V2Error("CORRELATION_MISMATCH", f"{field} differs from the task")
    return result


def dumps_result(result: dict, *, task: dict | None = None) -> bytes:
    return canonical(validate_result(result, task=task))


def loads_result(raw: bytes, *, task: dict | None = None) -> dict:
    if isinstance(raw, (bytes, bytearray)) and len(raw) > MAX_RESULT_BYTES:
        raise V2Error("SIZE_LIMIT", "result larger than MAX_RESULT_BYTES")
    result = loads_strict(raw)
    if canonical(result) != bytes(raw):
        raise V2Error("NON_CANONICAL", "result bytes are not canonical JSON")
    return validate_result(result, task=task)


def domain_payload(result: dict) -> bytes | None:
    """The exact domain result bytes (byte-identical to the adapter_api result), or None."""
    body = validate_result(result)["result"]
    return None if body is None else body["payload_canonical"].encode("utf-8")


__all__ = [
    "CLIENT_REF_SCHEMA",
    "DOMAINS",
    "MAX_REQUEST_BYTES",
    "MAX_RESULT_BYTES",
    "MAX_TASK_BYTES",
    "OUTCOME_CLASSES",
    "REGISTRY",
    "REGISTRY_SHA256",
    "RESULT_SCHEMA",
    "RESULT_STATUSES",
    "TASK_SCHEMA",
    "V2Error",
    "build_result",
    "build_task",
    "canonical",
    "client_ref_for",
    "digest",
    "domain_canonical",
    "domain_payload",
    "dumps_result",
    "dumps_task",
    "loads_result",
    "loads_strict",
    "loads_task",
    "request_bytes",
    "request_content_hash",
    "task_id_for",
    "validate_result",
    "validate_task",
]
