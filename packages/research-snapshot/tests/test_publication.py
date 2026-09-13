import copy

import pytest

from research_snapshot import canonical, confined, digest, loads, seal, validate
from research_snapshot.publication import publish


@pytest.fixture
def package():
    return seal(
        {
            "contract": "ResearchSnapshotV1",
            "profile": "local-evidence/1",
            "extensions": {},
            "origin": {
                "domain": "synthetic",
                "repository": "synthetic",
                "publisher": "test",
                "stream": "test",
                "code_revision": "test",
                "exporter_revision": "test",
                "inputs": {"source.md": "a" * 64},
            },
            "exported_at": "2026-09-13T00:00:00Z",
            "coverage": {
                "scope": "test",
                "completeness": "partial",
                "included": ["source.md"],
                "missing": [],
                "excluded": [],
                "limitations": ["synthetic only"],
            },
            "restrictions": {"policy": "test", "read": True, "disclose": False, "generate": False},
            "records": [],
            "evidence": [],
        }
    )


def test_publication_is_immutable_idempotent_and_cleans_staging(package, tmp_path):
    destination = tmp_path / "publication.json"
    receipt = publish(package, destination)
    original = destination.read_bytes()
    assert validate(loads(original)) == package
    assert receipt == digest(original)
    assert publish(package, destination) == receipt
    changed = copy.deepcopy(package)
    changed.pop("publication_id")
    changed["exported_at"] = "2026-09-13T00:00:01Z"
    with pytest.raises(FileExistsError, match="conflict"):
        publish(seal(changed), destination)
    assert destination.read_bytes() == original
    assert list(tmp_path.glob(".snapshot-*")) == []


def test_failed_link_does_not_publish_partial_file(package, tmp_path, monkeypatch):
    def unavailable(*args):
        raise OSError("synthetic unsupported hard link")

    monkeypatch.setattr("research_snapshot.publication.os.link", unavailable)
    with pytest.raises(OSError):
        publish(package, tmp_path / "publication.json")
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("field,value", [("profile", "unknown"), ("publication_id", "invalid")])
def test_invalid_contract_never_creates_destination(package, tmp_path, field, value):
    package[field] = value
    with pytest.raises(ValueError):
        publish(package, tmp_path / "publication.json")
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("path", ["../source.md", "/source.md", "C:/source.md", "a\\b"])
def test_path_escape_rejected(tmp_path, path):
    with pytest.raises(ValueError):
        confined(tmp_path, path)


def test_json_rejects_duplicate_keys_nonfinite_and_excessive_depth():
    for raw in [b'{"a":1,"a":2}', b'{"a":NaN}', b"[" * 20 + b"0" + b"]" * 20]:
        with pytest.raises(ValueError):
            loads(raw)


def test_received_evidence_hash_and_record_reference(package):
    body = {k: v for k, v in package.items() if k != "publication_id"}
    body["evidence"] = [
        {
            "id": "e1",
            "source": "source.md",
            "availability": "received",
            "text": "abc",
            "sha256": digest(b"abc"),
            "hash_basis": "received_utf8",
            "locator": "line 1",
            "start": 0,
            "end": 3,
            "offset_unit": "unicode_codepoints",
        }
    ]
    body["records"] = [
        {
            "source_id": "r1",
            "revision": "v1",
            "kind": "claim",
            "identity_basis": "source_assigned",
            "source_status": "UNKNOWN",
            "status_axis": "scientific",
            "mapping": None,
            "reason": None,
            "event_at": None,
            "recorded_at": None,
            "available_at": None,
            "supersedes": [],
            "evidence_ids": ["e1"],
        }
    ]
    assert validate(loads(canonical(seal(body))))["records"][0]["source_status"] == "UNKNOWN"
    body["evidence"][0]["text"] = "abd"
    with pytest.raises(ValueError, match="evidence hash"):
        validate(seal(body))
