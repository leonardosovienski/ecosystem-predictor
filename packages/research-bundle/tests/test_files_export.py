import errno
import os
import subprocess

import pytest
from research_bundle import digest
from research_bundle.export import admitted_sources
from research_bundle.files import _posix_open, safe_open, transfer


def test_directory_chain_synced_before_descendants(tmp_path, monkeypatch):
    from research_bundle import files

    target = tmp_path / "cas" / "sha256" / "ab"
    synced = []

    def sync(parent):
        if parent == tmp_path:
            assert (tmp_path / "cas").is_dir()
            assert not (tmp_path / "cas/sha256").exists()
        synced.append(parent)

    monkeypatch.setattr(files, "fsync_dir", sync)
    files.safe_mkdirs(target)
    assert synced[-3:] == [tmp_path, tmp_path / "cas", tmp_path / "cas/sha256"]
    # Existing entries are synchronized on retries, too.
    monkeypatch.setattr(files, "fsync_dir", synced.append)
    files.safe_mkdirs(target)
    assert synced[-3:] == [tmp_path, tmp_path / "cas", tmp_path / "cas/sha256"]


def test_provenance_tracks_dependency_bytes_and_builder_has_no_domain_defaults(tmp_path, monkeypatch):
    import research_bundle
    from research_bundle import canonical
    from research_bundle.export import Builder, exporter_provenance

    package = tmp_path / "package"
    package.mkdir()
    module = package / "__init__.py"
    module.write_bytes(b"# shared code v1")
    monkeypatch.setattr(research_bundle, "__file__", str(module))
    producer = tmp_path / "producer.py"
    producer.write_bytes(b"# producer")
    first = exporter_provenance({"producer.py": producer})
    module.write_bytes(b"# shared code v2")
    second = exporter_provenance({"producer.py": producer})
    assert first["producer_files"] == second["producer_files"]
    assert digest(canonical(first)) != digest(canonical(second))
    origin = dict(
        domain="unrelated",
        repository="urn:explicit",
        publisher="chosen",
        stream="owned",
        code_revision="code",
        exporter_revision="sha256:" + digest(canonical(second)),
        inputs={"input.json": "0" * 64},
    )
    restrictions = dict(policy="receiver-selected", read=True, disclose=False, generate=False)
    builder = Builder(origin, restrictions, "2026-09-12T00:00:00Z", provenance=second)
    assert builder.body["origin"] == origin and builder.body["restrictions"] == restrictions
    assert builder.body["evidence"][0]["payload"] == second


@pytest.mark.parametrize("code", [errno.ELOOP, errno.ENOTDIR, errno.ENOENT])
def test_posix_path_errors(monkeypatch, code):
    error = OSError(code, "injected")

    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr(os, "open", fail)
    if code == errno.ENOENT:
        with pytest.raises(OSError) as caught:
            _posix_open("missing", os.O_RDONLY)
        assert caught.value is error
    else:
        with pytest.raises(ValueError, match="UNSAFE_PATH") as caught:
            _posix_open("unsafe", os.O_RDONLY)
        assert caught.value.__cause__ is error


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
