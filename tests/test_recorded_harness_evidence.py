import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "recorded_drift", Path(__file__).resolve().parents[1] / "scripts/check_ecosystem_drift.py"
)
assert spec and spec.loader
drift = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drift)


def fixture_record(tmp_path):
    evidence = dict(
        schema_version="pipeline-power/2",
        core_version="3.2.1",
        code_version="git:" + "a" * 40,
        passed_at="2026-09-12T00:00:00Z",
        expires_at="2026-09-19T00:00:00Z",
        metric="psr",
        pipeline_fingerprint="b" * 64,
    )
    raw = json.dumps(evidence).encode()
    (tmp_path / "control.json").write_bytes(raw)
    return dict(
        repo="cripto-predictor",
        evidence_path="control.json",
        evidence_sha256=hashlib.sha256(raw).hexdigest(),
        harness_version=evidence["schema_version"],
        reported_core_version=evidence["core_version"],
        domain_code_version=evidence["code_version"],
        executed_at=evidence["passed_at"],
        expires_at=evidence["expires_at"],
        metric=evidence["metric"],
        pipeline_fingerprint=evidence["pipeline_fingerprint"],
    )


def test_matching_recorded_control_passes(tmp_path):
    assert drift.check_recorded_evidence(fixture_record(tmp_path), tmp_path) == []


@pytest.mark.parametrize(
    "field,value",
    [
        ("evidence_sha256", "0" * 64),
        ("reported_core_version", "3.2.0"),
        ("domain_code_version", "git:" + "c" * 40),
        ("metric", "different"),
        ("pipeline_fingerprint", None),
        ("expires_at", "2099-01-01"),
    ],
)
def test_mismatch_is_refused(tmp_path, field, value):
    record = fixture_record(tmp_path)
    record[field] = value
    assert drift.check_recorded_evidence(record, tmp_path)


def test_missing_and_outside_evidence_are_refused(tmp_path):
    record = fixture_record(tmp_path)
    for path in ("missing.json", "../control.json", str((tmp_path / "control.json").resolve())):
        record["evidence_path"] = path
        assert drift.check_recorded_evidence(record, tmp_path)
