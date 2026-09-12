"""ResearchBundleV1: pure contract, no domain or receiver imports.

Canonical bytes use ResearchSnapshotV1's serializer unchanged. Array order and
nulls are significant; strings are not Unicode-normalized. JSON numbers use
Python's finite JSON representation; integers are bounded to signed 64 bits.
"""

import json
import math
import re

from research_snapshot import canonical, digest, keys, string, strings, timestamp

VERSION = "ResearchBundleV1"
PROFILE = "local-research/1"
MAX_BYTES = 2_000_000
MAX_ENTITIES = 200
MAX_EVIDENCE = 200
MAX_ARTIFACTS = 200
MAX_RELATIONS = 800
MAX_DEPTH = 18
MAX_PAYLOAD = 100_000
MAX_OBJECT = 16_000_000
MAX_RECEIVED = 64_000_000
ROLES = set(
    (
        "dataset_slice document trade_ledger prediction_set settlement_set feature_slice "
        "model_artifact report attestation log other"
    ).split()
)
RELATIONS = set(
    (
        "REPRESENTED_BY REFERENCES USES_DATASET HAS_TRIAL HAS_ATTESTATION EVALUATED_BY "
        "SUPPORTS SUPPORTED_BY HAS_VERDICT PREDICTS USES PRODUCED_BY SETTLED_BY SUPERSEDES"
    ).split()
)
ENTITY_FIELDS = (
    "entity_id revision entity_type identity_basis status status_axis event_at "
    "recorded_at available_at payload supersedes evidence_ids"
)
ARTIFACT_FIELDS = (
    "artifact_id role availability media_type sha256 size relative_path locator logical_name metadata"
)
ENDPOINT_FIELDS = "kind namespace id revision external"


def bounded(value, depth=0):
    if depth > MAX_DEPTH:
        raise ValueError("CONTRACT_INVALID: depth")
    if type(value) is dict:
        for key, child in value.items():
            string(key, limit=500)
            bounded(child, depth + 1)
    elif type(value) is list:
        for child in value:
            bounded(child, depth + 1)
    elif type(value) is str:
        if len(value.encode("utf-8")) > MAX_PAYLOAD:
            raise ValueError("CONTRACT_INVALID: string size")
    elif type(value) is int:
        if not -(2**63) <= value < 2**63:
            raise ValueError("CONTRACT_INVALID: integer range")
    elif type(value) is float:
        if not math.isfinite(value):
            raise ValueError("CONTRACT_INVALID: nonfinite")
    elif value is not None and type(value) is not bool:
        raise ValueError("CONTRACT_INVALID: non JSON value")


def loads(raw):
    if type(raw) is not bytes or len(raw) > MAX_BYTES:
        raise ValueError("CONTRACT_INVALID: manifest bytes")

    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("CONTRACT_INVALID: duplicate key")
            result[key] = value
        return result

    def nonfinite(_):
        raise ValueError("CONTRACT_INVALID: nonfinite")

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique, parse_constant=nonfinite)
        bounded(value)
        return value
    except (UnicodeError, RecursionError) as exc:
        raise ValueError("CONTRACT_INVALID: encoding/depth") from exc


def sha(value, nullable=False):
    if value is None and nullable:
        return
    if type(value) is not str or not re.fullmatch(r"[a-f0-9]{64}", value):
        raise ValueError("CONTRACT_INVALID: SHA256")


def safe_path(value):
    string(value)
    if any(c in value for c in '\\:<>"|?*') or value.startswith("/"):
        raise ValueError("CONTRACT_INVALID: path")
    for part in value.split("/"):
        if (
            part in {"", ".", ".."}
            or part.endswith((" ", "."))
            or any(ord(c) < 32 for c in part)
            or re.fullmatch(r"(?i)(con|prn|aux|nul|com[0-9]|lpt[0-9])(?:\..*)?", part)
        ):
            raise ValueError("CONTRACT_INVALID: path")
    return value


def vocabulary(value, registered):
    string(value, limit=100)
    if value not in registered and not re.fullmatch(
        r"[a-z][a-z0-9_.-]{1,39}:[A-Za-z][A-Za-z0-9_.-]{0,49}", value
    ):
        raise ValueError("CONTRACT_INVALID: unregistered vocabulary")


def namespace(origin):
    return [origin[k] for k in ("domain", "repository", "publisher", "stream")]


def entity_key(origin, entity):
    return digest(canonical(namespace(origin) + [entity["entity_id"], entity["revision"]]))


def signature(bundle, entity):
    evidence = {e["id"]: e for e in bundle["evidence"]}
    return digest(canonical([entity, [evidence[k] for k in entity["evidence_ids"]]]))


def endpoint(kind, origin, identity, revision=None, external=False):
    return dict(kind=kind, namespace=namespace(origin), id=identity, revision=revision, external=external)


def seal(body):
    body = {k: v for k, v in body.items() if k != "bundle_id"}
    bounded(body)
    return {**body, "bundle_id": digest(canonical(body))}


def validate(bundle):
    bounded(bundle)
    keys(
        bundle,
        "contract profile bundle_id origin exported_at coverage restrictions "
        "entities evidence artifacts relations",
    )
    if bundle["contract"] != VERSION or bundle["profile"] != PROFILE:
        raise ValueError("CONTRACT_INVALID: version/profile")
    sha(bundle["bundle_id"])
    if len(canonical(bundle)) > MAX_BYTES:
        raise ValueError("CONTRACT_INVALID: manifest size")
    origin = bundle["origin"]
    keys(origin, "domain repository publisher stream code_revision exporter_revision inputs")
    for k in ("domain", "repository", "publisher", "stream", "code_revision", "exporter_revision"):
        string(origin[k])
    if type(origin["inputs"]) is not dict or not 1 <= len(origin["inputs"]) <= 30:
        raise ValueError("CONTRACT_INVALID: inputs")
    for path, value in origin["inputs"].items():
        safe_path(path)
        sha(value)

    # An ISO calendar timestamp with an explicit offset; never import time.
    def clock(value, nullable=False):
        if value is None and nullable:
            return
        if type(value) is not str or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})", value
        ):
            raise ValueError("CONTRACT_INVALID: timestamp")
        if value[-1] != "Z" and (int(value[-5:-3]) > 23 or int(value[-2:]) > 59):
            raise ValueError("CONTRACT_INVALID: timestamp offset")
        timestamp(value)

    clock(bundle["exported_at"])
    coverage = bundle["coverage"]
    keys(coverage, "scope completeness included missing excluded limitations")
    string(coverage["scope"])
    if coverage["completeness"] not in ("partial", "complete_declared_scope"):
        raise ValueError("CONTRACT_INVALID: completeness")
    for k in ("included", "missing", "excluded", "limitations"):
        strings(coverage[k])
    if set(coverage["included"]) != set(origin["inputs"]):
        raise ValueError("CONTRACT_INVALID: input coverage")
    restrictions = bundle["restrictions"]
    keys(restrictions, "policy read disclose generate")
    string(restrictions["policy"])
    if any(type(restrictions[k]) is not bool for k in ("read", "disclose", "generate")):
        raise ValueError("CONTRACT_INVALID: restrictions")
    for field, cap in (
        ("entities", MAX_ENTITIES),
        ("evidence", MAX_EVIDENCE),
        ("artifacts", MAX_ARTIFACTS),
        ("relations", MAX_RELATIONS),
    ):
        if type(bundle[field]) is not list or len(bundle[field]) > cap:
            raise ValueError("CONTRACT_INVALID: " + field + " cap")
    evidence = set()
    for item in bundle["evidence"]:
        keys(item, "id source locator payload")
        string(item["id"])
        string(item["locator"])
        if item["id"] in evidence or item["source"] not in origin["inputs"]:
            raise ValueError("CONTRACT_INVALID: evidence identity/source")
        if type(item["payload"]) is not dict or len(canonical(item["payload"])) > MAX_PAYLOAD:
            raise ValueError("CONTRACT_INVALID: evidence payload")
        evidence.add(item["id"])
    entities = set()
    for item in bundle["entities"]:
        keys(item, ENTITY_FIELDS)
        for k in ("entity_id", "revision", "entity_type", "identity_basis", "status", "status_axis"):
            string(item[k])
        for k in ("event_at", "recorded_at", "available_at"):
            clock(item[k], True)
        strings(item["supersedes"])
        strings(item["evidence_ids"])
        identity = (item["entity_id"], item["revision"])
        if identity in entities or item["revision"] in item["supersedes"]:
            raise ValueError("CONTRACT_INVALID: duplicate/self supersession")
        if not set(item["evidence_ids"]) <= evidence:
            raise ValueError("CONTRACT_INVALID: evidence link")
        if type(item["payload"]) is not dict or len(canonical(item["payload"])) > MAX_PAYLOAD:
            raise ValueError("CONTRACT_INVALID: entity payload")
        entities.add(identity)
    artifacts, received, paths = set(), 0, set()
    for item in bundle["artifacts"]:
        keys(item, ARTIFACT_FIELDS)
        for k in ("artifact_id", "logical_name"):
            string(item[k])
        string(item["locator"], nullable=True)
        if item["artifact_id"] in artifacts:
            raise ValueError("CONTRACT_INVALID: duplicate artifact")
        artifacts.add(item["artifact_id"])
        vocabulary(item["role"], ROLES)
        if type(item["media_type"]) is not str or not re.fullmatch(
            r"[a-z0-9][a-z0-9!#$&^_.+-]*/[a-z0-9][a-z0-9!#$&^_.+-]*", item["media_type"]
        ):
            raise ValueError("CONTRACT_INVALID: media type")
        sha(item["sha256"], True)
        if item["size"] is not None and (type(item["size"]) is not int or not 0 <= item["size"] < 2**63):
            raise ValueError("CONTRACT_INVALID: size")
        if type(item["metadata"]) is not dict or len(canonical(item["metadata"])) > MAX_PAYLOAD:
            raise ValueError("CONTRACT_INVALID: resource metadata")
        if item["availability"] == "received":
            sha(item["sha256"])
            safe_path(item["relative_path"])
            if item["relative_path"] in paths or item["size"] is None or item["size"] > MAX_OBJECT:
                raise ValueError("CONTRACT_INVALID: received declaration")
            paths.add(item["relative_path"])
            received += item["size"]
        elif item["availability"] == "reference_only":
            if item["relative_path"] is not None or item["locator"] is None:
                raise ValueError("CONTRACT_INVALID: reference masquerade")
        else:
            raise ValueError("CONTRACT_INVALID: availability")
    if received > MAX_RECEIVED:
        raise ValueError("CONTRACT_INVALID: received total")
    relation_ids = set()
    for item in bundle["relations"]:
        keys(item, "relation_id type source target")
        string(item["relation_id"])
        if item["relation_id"] in relation_ids:
            raise ValueError("CONTRACT_INVALID: duplicate relation")
        relation_ids.add(item["relation_id"])
        vocabulary(item["type"], RELATIONS)
        for ep in (item["source"], item["target"]):
            keys(ep, ENDPOINT_FIELDS)
            string(ep["id"])
            if type(ep["namespace"]) is not list or len(ep["namespace"]) != 4:
                raise ValueError("CONTRACT_INVALID: namespace")
            for val in ep["namespace"]:
                string(val)
            if type(ep["external"]) is not bool or ep["kind"] not in ("entity", "artifact"):
                raise ValueError("CONTRACT_INVALID: endpoint")
            if ep["kind"] == "entity":
                string(ep["revision"])
                exists = (ep["id"], ep["revision"]) in entities
            else:
                if ep["revision"] is not None:
                    raise ValueError("CONTRACT_INVALID: artifact revision")
                exists = ep["id"] in artifacts
            if not ep["external"] and (ep["namespace"] != namespace(origin) or not exists):
                raise ValueError("CONTRACT_INVALID: dangling local endpoint")
        if item["type"] == "SUPERSEDES" and item["source"] == item["target"]:
            raise ValueError("CONTRACT_INVALID: self supersession")
    if seal(bundle)["bundle_id"] != bundle["bundle_id"]:
        raise ValueError("CONTRACT_INVALID: bundle hash")
    return bundle
