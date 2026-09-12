import os
import subprocess

import pytest
from research_bundle import digest
from research_bundle.export import admitted_sources
from research_bundle.files import safe_open, transfer


@pytest.fixture
def source(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", str(root)], check=True, capture_output=True)
    (root / "report.json").write_bytes(b'{"status":"UNKNOWN"}')
    subprocess.run(["git", "-C", str(root), "add", "report.json"], check=True, capture_output=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.invalid",
            "commit",
            "-m",
            "fixture",
        ],
        check=True,
        capture_output=True,
    )
    return root


def test_pinned_read_only(source):
    expected = digest((source / "report.json").read_bytes())
    _, sources = admitted_sources(source, {"report.json": expected}, {"report.json"})
    assert sources["report.json"] == b'{"status":"UNKNOWN"}'
    assert not subprocess.check_output(["git", "-C", str(source), "status", "--porcelain"])


@pytest.mark.parametrize("mode", ["unlisted", "wrong_hash", "missing", "uncommitted", "secret"])
def test_source_rejection(source, mode):
    expected = {"report.json": digest((source / "report.json").read_bytes())}
    if mode == "unlisted":
        expected = {"private.env": "0" * 64}
    if mode == "wrong_hash":
        expected = {"report.json": "0" * 64}
    if mode == "missing":
        (source / "report.json").unlink()
    if mode in {"uncommitted", "secret"}:
        (source / "report.json").write_bytes(b'{"api_key":"FAKE_SECRET_TEST_ONLY"}')
        if mode == "secret":
            subprocess.run(["git", "-C", str(source), "add", "."], check=True, capture_output=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(source),
                    "-c",
                    "user.name=Test",
                    "-c",
                    "user.email=test@example.invalid",
                    "commit",
                    "-m",
                    "fixture",
                ],
                check=True,
                capture_output=True,
            )
            expected["report.json"] = digest((source / "report.json").read_bytes())
    with pytest.raises((ValueError, OSError)):
        admitted_sources(source, expected, {"report.json"})


def test_open_handle_mutation_protection(source):
    with safe_open(source, "report.json") as handle:
        if os.name == "nt":
            with pytest.raises(OSError):
                (source / "report.json").write_bytes(b"changed")
            transfer(handle, limit=1000, expected_sha=digest(b'{"status":"UNKNOWN"}'))
        else:
            (source / "report.json").write_bytes(b"changed")
            with pytest.raises(ValueError):
                transfer(handle, limit=1000, expected_sha=digest(b'{"status":"UNKNOWN"}'))
