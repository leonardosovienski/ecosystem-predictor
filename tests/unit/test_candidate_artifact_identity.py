"""A candidate wheel must never pass on nominal version alone."""

import json
import runpy
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[2]
matches = runpy.run_path(str(ROOT / "scripts/check_real_plugin_integration.py"))["candidate_matches"]


@pytest.mark.parametrize(
    ("expected", "direct", "version", "valid"),
    [
        ({"wheel_sha256": "a" * 64}, {"archive_info": {"hashes": {"sha256": "a" * 64}}}, "1", True),
        ({"wheel_sha256": "a" * 64}, {"archive_info": {"hashes": {"sha256": "b" * 64}}}, "1", False),
        ({"wheel_sha256": "a" * 64}, {}, "1", False),
        ({"wheel_sha256": "a" * 64}, {"archive_info": {"hashes": {"sha256": "a" * 64}}}, "2", False),
        ({"wheel_sha256": None}, {}, "1", False),
        ({"commit": "a" * 40}, {"vcs_info": {"commit_id": "a" * 40}}, "1", True),
        ({"commit": "a" * 40}, {"vcs_info": {"commit_id": "b" * 40}}, "1", False),
        ({"commit": None}, {}, "1", False),
    ],
)
def test_requires_exact_artifact_provenance(expected, direct, version, valid):
    distribution = SimpleNamespace(version=version, read_text=lambda name: json.dumps(direct))
    assert matches(distribution, {"version": "1", **expected}) is valid
