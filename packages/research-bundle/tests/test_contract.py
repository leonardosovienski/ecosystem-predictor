import copy
import json

import pytest
from research_bundle import canonical, digest, endpoint, loads, seal, validate


def fixture():
    origin = dict(
        domain="test",
        repository="test/repo",
        publisher="test",
        stream="test",
        code_revision="test-code",
        exporter_revision="test-exporter",
        inputs={"report.json": "0" * 64},
    )
    entity = dict(
        entity_id="TEST-HYPOTHESIS-001",
        revision="1",
        entity_type="hypothesis",
        identity_basis="source_assigned",
        status="UNKNOWN",
        status_axis="scientific",
        event_at=None,
        recorded_at=None,
        available_at=None,
        payload={"unknown": None},
        supersedes=[],
        evidence_ids=["e1"],
    )
    return seal(
        dict(
            contract="ResearchBundleV1",
            profile="local-research/1",
            origin=origin,
            exported_at="2026-09-11T00:00:00Z",
            restrictions=dict(policy="test/1", read=True, disclose=False, generate=False),
            coverage=dict(
                scope="test",
                completeness="partial",
                included=["report.json"],
                missing=[],
                excluded=[],
                limitations=["test fixture"],
            ),
            entities=[entity],
            evidence=[dict(id="e1", source="report.json", locator="/", payload={})],
            artifacts=[
                dict(
                    artifact_id="a1",
                    role="document",
                    availability="received",
                    media_type="text/plain",
                    sha256=digest(b"real test bytes"),
                    size=15,
                    relative_path="files/report.txt",
                    locator=None,
                    logical_name="report",
                    metadata={"license": "UNKNOWN"},
                )
            ],
            relations=[
                dict(
                    relation_id="r1",
                    type="SUPPORTED_BY",
                    source=endpoint("entity", origin, entity["entity_id"], "1"),
                    target=endpoint("artifact", origin, "a1"),
                )
            ],
        )
    )


def test_canonical_and_identity():
    bundle = fixture()
    assert validate(loads(canonical(bundle))) == bundle
    assert seal(bundle) == bundle
    assert loads(json.dumps(bundle, indent=2).encode()) == bundle
    assert digest(canonical(bundle)) != digest(json.dumps(bundle, indent=2).encode())
    assert bundle["entities"][0]["event_at"] is None


@pytest.mark.parametrize(
    "raw",
    [
        b'{"a":1,"a":2}',
        b'{"a":NaN}',
        b'{"a":Infinity}',
        b'{"a":-Infinity}',
        b'{"a":1e999}',
        b'"\xff"',
        b'"\\ud800"',
        b"[" * 1000 + b"]" * 1000,
        b'"' + b"a" * 2_000_001 + b'"',
    ],
    ids=[
        "duplicate",
        "nan",
        "infinity",
        "negative-infinity",
        "overflow",
        "utf8",
        "surrogate",
        "depth",
        "oversize",
    ],
)
def test_strict_parse(raw):
    with pytest.raises(ValueError):
        loads(raw)


@pytest.mark.parametrize(
    "path",
    [
        "../a",
        "/a",
        "C:/a",
        "C:a",
        "\\\\host\\a",
        "a\\b",
        "a/../b",
        "a//b",
        "a/.",
        "NUL.txt",
        "a.",
        "a ",
        "a\x00",
    ],
)
def test_paths(path):
    b = fixture()
    b["artifacts"][0]["relative_path"] = path
    with pytest.raises(ValueError):
        validate(seal(b))


@pytest.mark.parametrize(
    "field,value",
    [
        ("sha256", "X" * 64),
        ("sha256", None),
        ("size", True),
        ("size", -1),
        ("size", None),
        ("size", 16_000_001),
        ("relative_path", None),
        ("media_type", "text/html\r\nX: malicious"),
        ("role", "anything"),
        ("availability", "unknown"),
    ],
)
def test_resource_errors(field, value):
    b = fixture()
    b["artifacts"][0][field] = value
    with pytest.raises(ValueError):
        validate(seal(b))


def test_reference_and_external():
    b = fixture()
    a = b["artifacts"][0]
    a.update(
        availability="reference_only",
        relative_path=None,
        locator="opaque://not-fetched",
        sha256=None,
        size=None,
    )
    assert validate(seal(b))
    b["relations"][0]["target"].update(id="outside", external=True)
    assert validate(seal(b))
    b["relations"][0]["target"]["external"] = False
    with pytest.raises(ValueError):
        validate(seal(b))


@pytest.mark.parametrize(
    "mode",
    [
        "unknown",
        "missing",
        "clock",
        "self",
        "evidence",
        "duplicate_entity",
        "duplicate_artifact",
        "duplicate_relation",
        "reference_path",
        "payload",
        "namespace",
        "hash",
    ],
)
def test_invariants(mode):
    b = fixture()
    if mode == "unknown":
        b["unexpected"] = 1
    if mode == "missing":
        del b["coverage"]
    if mode == "clock":
        b["entities"][0]["event_at"] = "2026-09-11"
    if mode == "self":
        b["entities"][0]["supersedes"] = ["1"]
    if mode == "evidence":
        b["entities"][0]["evidence_ids"] = ["absent"]
    if mode == "duplicate_entity":
        b["entities"] *= 2
    if mode == "duplicate_artifact":
        b["artifacts"] *= 2
    if mode == "duplicate_relation":
        b["relations"] *= 2
    if mode == "reference_path":
        b["artifacts"][0].update(availability="reference_only", locator="opaque")
    if mode == "payload":
        b["entities"][0]["payload"] = {"too_long": "a" * 100001}
    if mode == "namespace":
        b["relations"][0]["source"]["namespace"][0] = "other"
    if mode == "hash":
        b["bundle_id"] = "1" * 64
    with pytest.raises((ValueError, KeyError)):
        validate(b if mode == "hash" else seal(b))


@pytest.mark.parametrize(
    "field,cap", [("entities", 200), ("evidence", 200), ("artifacts", 200), ("relations", 800)]
)
def test_counts(field, cap):
    b = fixture()
    b[field] = [copy.deepcopy(b[field][0]) for _ in range(cap + 1)]
    with pytest.raises(ValueError):
        validate(seal(b))
