"""Canonical ResearchSnapshotV1 validator. Pure stdlib, no domain imports."""

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

VERSION = "ResearchSnapshotV1"
PROFILE = "local-evidence/1"
MAX_BYTES = 2_000_000
MAX_RECORDS = 200


def canonical(value):
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def digest(value):
    return hashlib.sha256(value).hexdigest()


def keys(value, required):
    if type(value) is not dict or set(value) != set(required.split()):
        raise ValueError("CONTRACT_INVALID: unexpected or missing fields")


def string(value, nullable=False, limit=500):
    if nullable and value is None:
        return
    if type(value) is not str or not value.strip() or len(value) > limit:
        raise ValueError("CONTRACT_INVALID: invalid string")


def strings(value, limit=200):
    if type(value) is not list or len(value) > limit:
        raise ValueError("CONTRACT_INVALID: invalid list")
    for item in value:
        string(item)
    if len(set(value)) != len(value):
        raise ValueError("CONTRACT_INVALID: duplicate list item")


def timestamp(value, nullable=False):
    if value is None and nullable:
        return
    string(value)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("timezone required")
    except ValueError as exc:
        raise ValueError("CONTRACT_INVALID: timestamp must include timezone") from exc


def safe_path(value):
    string(value)
    if (
        "\\" in value
        or ":" in value
        or value.startswith("/")
        or any(p in {"", ".", ".."} for p in value.split("/"))
    ):
        raise ValueError("CONTRACT_INVALID: unsafe relative path")
    return value


def confined(root, relative):
    safe_path(relative)
    root = Path(root).resolve(strict=True)
    candidate = root / relative
    # Reject all links/junctions, including links pointing inside the root.
    current = candidate
    while current != root:
        if current.is_symlink() or (hasattr(current, "is_junction") and current.is_junction()):
            raise ValueError("Unauthorized link")
        current = current.parent
    resolved = candidate.resolve(strict=True)
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise ValueError("Unauthorized path")
    return resolved


def loads(raw):
    if len(raw) > MAX_BYTES:
        raise ValueError("CONTRACT_INVALID: publication byte limit")

    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("CONTRACT_INVALID: duplicate JSON key")
            result[key] = value
        return result

    try:
        value = json.loads(
            raw,
            object_pairs_hook=unique,
            parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Nonfinite")),
        )

        def depth(item, level=0):
            if level > 18:
                raise ValueError("CONTRACT_INVALID: depth limit")
            if isinstance(item, dict):
                for child in item.values():
                    depth(child, level + 1)
            elif isinstance(item, list):
                for child in item:
                    depth(child, level + 1)

        depth(value)
        return value
    except (RecursionError, UnicodeError) as exc:
        raise ValueError("CONTRACT_INVALID: invalid encoding/depth") from exc


def seal(body):
    return {**body, "publication_id": digest(canonical(body))}


def validate(package):
    keys(
        package,
        "contract profile extensions publication_id origin exported_at "
        "coverage restrictions records evidence",
    )
    if package["contract"] != VERSION or package["profile"] != PROFILE:
        raise ValueError("CONTRACT_INVALID: incompatible version/profile")
    if type(package["extensions"]) is not dict or len(package["extensions"]) > 10:
        raise ValueError("CONTRACT_INVALID: extensions")
    for name, extension in package["extensions"].items():
        string(name)
        keys(extension, "required payload")
        if extension["required"] is not False:
            raise ValueError("CONTRACT_INVALID: unsupported required extension")
    if (
        digest(canonical({k: v for k, v in package.items() if k != "publication_id"}))
        != package["publication_id"]
    ):
        raise ValueError("CONTRACT_INVALID: publication hash mismatch")
    origin = package["origin"]
    keys(origin, "domain repository publisher stream code_revision exporter_revision inputs")
    for key in ("domain", "repository", "publisher", "stream", "code_revision", "exporter_revision"):
        string(origin[key])
    if type(origin["inputs"]) is not dict or not origin["inputs"] or len(origin["inputs"]) > 30:
        raise ValueError("CONTRACT_INVALID: inputs")
    for path, sha in origin["inputs"].items():
        safe_path(path)
        if type(sha) is not str or not re.fullmatch("[a-f0-9]{64}", sha):
            raise ValueError("CONTRACT_INVALID: input hash")
    timestamp(package["exported_at"])
    coverage = package["coverage"]
    keys(coverage, "scope completeness included missing excluded limitations")
    string(coverage["scope"])
    if coverage["completeness"] not in {"partial", "complete_declared_scope"}:
        raise ValueError("CONTRACT_INVALID: completeness")
    for key in ("included", "missing", "excluded", "limitations"):
        strings(coverage[key])
    if set(coverage["included"]) != set(origin["inputs"]):
        raise ValueError("CONTRACT_INVALID: coverage inputs mismatch")
    restrictions = package["restrictions"]
    keys(restrictions, "policy read disclose generate")
    string(restrictions["policy"])
    for key in ("read", "disclose", "generate"):
        if type(restrictions[key]) is not bool:
            raise ValueError("CONTRACT_INVALID: restriction type")
    if type(package["evidence"]) is not list or len(package["evidence"]) > 200:
        raise ValueError("CONTRACT_INVALID: evidence limit")
    evidence = {}
    for item in package["evidence"]:
        keys(item, "id source availability text sha256 hash_basis locator start end offset_unit")
        string(item["id"])
        if item["id"] in evidence or item["source"] not in origin["inputs"]:
            raise ValueError("CONTRACT_INVALID: evidence identity/source")
        string(item["locator"])
        if item["availability"] == "received":
            string(item["text"], limit=100_000)
            if item["hash_basis"] != "received_utf8" or item["offset_unit"] != "unicode_codepoints":
                raise ValueError("CONTRACT_INVALID: hash/offset basis")
            if (
                type(item["start"]) is not int
                or type(item["end"]) is not int
                or item["start"] < 0
                or item["end"] - item["start"] != len(item["text"])
            ):
                raise ValueError("CONTRACT_INVALID: excerpt offsets")
            if digest(item["text"].encode("utf-8")) != item["sha256"]:
                raise ValueError("CONTRACT_INVALID: evidence hash mismatch")
        elif item["availability"] == "reference_only":
            if any(
                item[k] is not None for k in ("text", "sha256", "hash_basis", "start", "end", "offset_unit")
            ):
                raise ValueError("CONTRACT_INVALID: reference masquerading as content")
        else:
            raise ValueError("CONTRACT_INVALID: evidence availability")
        evidence[item["id"]] = item
    if type(package["records"]) is not list or len(package["records"]) > MAX_RECORDS:
        raise ValueError("CONTRACT_INVALID: record limit")
    identities = set()
    for record in package["records"]:
        keys(
            record,
            "source_id revision kind identity_basis source_status status_axis mapping reason "
            "event_at recorded_at available_at supersedes evidence_ids",
        )
        for key in ("source_id", "revision", "kind", "source_status", "status_axis"):
            string(record[key])
        if record["identity_basis"] not in {"source_assigned", "document_identity", "ambiguous_observation"}:
            raise ValueError("CONTRACT_INVALID: identity basis")
        if record["status_axis"] not in {
            "scientific",
            "operational",
            "predictive",
            "economic",
            "source_availability",
            "domain_lifecycle",
        }:
            raise ValueError("CONTRACT_INVALID: status axis")
        for key in ("reason", "event_at", "recorded_at", "available_at"):
            string(record[key], nullable=True, limit=2000)
        for key in ("event_at", "recorded_at", "available_at"):
            timestamp(record[key], nullable=True)
        if record["mapping"] is not None:
            keys(record["mapping"], "value axis version origin")
            for val in record["mapping"].values():
                string(val)
        strings(record["supersedes"])
        if record["revision"] in record["supersedes"]:
            raise ValueError("CONTRACT_INVALID: self-superseding revision")
        strings(record["evidence_ids"])
        if not record["evidence_ids"] or not set(record["evidence_ids"]) <= evidence.keys():
            raise ValueError("CONTRACT_INVALID: unknown evidence")
        identity = (record["source_id"], record["revision"])
        if identity in identities:
            raise ValueError("CONTRACT_INVALID: duplicate occurrence revision")
        identities.add(identity)
    if len(canonical(package)) > MAX_BYTES:
        raise ValueError("CONTRACT_INVALID: publication byte limit")
    return package
