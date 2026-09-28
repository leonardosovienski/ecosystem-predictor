"""Renovação agendada do harness do cripto: decide quando renovar e registra só atestados genuínos.

O resultado de `apply` é conferido pelas próprias regras do `check_ecosystem_drift` (evidência com hash e
campos iguais ao atestado; nenhum ALIGNED vencido), sobre uma cópia do registry real.
"""

import importlib.util
import json
import shutil
from datetime import datetime
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]


def _module(name: str, script: str):
    spec = importlib.util.spec_from_file_location(name, _ROOT / "scripts" / script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


renewal = _module("renew_crypto_harness", "renew_crypto_harness.py")
drift = _module("ecosystem_drift_check_for_renewal", "check_ecosystem_drift.py")
CONFIG = json.loads((_ROOT / "registries" / "harness_renewal.json").read_text(encoding="utf-8"))
COMMIT = CONFIG["source"]["commit"]


def _at(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


@pytest.fixture
def root(tmp_path: Path) -> Path:
    (tmp_path / "registries").mkdir()
    for name in ("harness_registry.json", "harness_renewal.json"):
        shutil.copy(_ROOT / "registries" / name, tmp_path / "registries" / name)
    shutil.copytree(_ROOT / "docs" / "engineering_controls", tmp_path / "docs" / "engineering_controls")
    return tmp_path


def _registry(root: Path) -> dict:
    return json.loads((root / "registries" / "harness_registry.json").read_text(encoding="utf-8"))


def _write_attestations(folder: Path, passed_at: str, expires_at: str, commit: str = COMMIT) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    for metric, name, fingerprint in (
        ("psr", "trials.harness_attestation.json", "a" * 64),
        ("spearman_ic", "trials.phase1_harness_attestation.json", "b" * 64),
    ):
        doc = {
            "schema_version": "pipeline-power/2",
            "passed_at": passed_at,
            "expires_at": expires_at,
            "core_version": "3.2.1",
            "code_version": f"package:3.2.1;git:{commit}",
            "metric": metric,
            "pipeline_fingerprint": fingerprint,
        }
        (folder / name).write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")


def _latest_aligned_expiry(registry: dict) -> datetime:
    return max(_at(item["expires_at"]) for item in renewal._aligned(registry))


def test_decide_renews_only_inside_the_window_and_flags_expired(root: Path) -> None:
    registry = _registry(root)
    expiry = _latest_aligned_expiry(registry)
    hours = CONFIG["renew_when_valid_for_less_than_hours"]
    early = expiry - renewal.timedelta(hours=hours + 1)
    late = expiry - renewal.timedelta(hours=hours - 1)
    assert renewal.decide(registry, CONFIG, early) == {
        "renew": False,
        "expired": False,
        "expired_evidence": [],
    }
    assert renewal.decide(registry, CONFIG, late)["renew"] is True
    after = renewal.decide(registry, CONFIG, expiry + renewal.timedelta(seconds=1))
    assert after["renew"] is True and after["expired"] is True


def test_apply_registers_the_reissue_and_the_drift_check_accepts_it(root: Path) -> None:
    registry = _registry(root)
    now = _latest_aligned_expiry(registry) - renewal.timedelta(hours=24)
    before = [item["evidence_path"] for item in renewal._aligned(registry)]
    folder = root / "staged"
    _write_attestations(folder, "2026-10-04T00:00:00Z", "2026-10-11T00:00:00Z")
    changed = renewal.apply(root, registry, CONFIG, now, folder)
    day = now.strftime("%Y%m%d")
    assert changed["superseded"] == before and changed["expired"] == []
    assert changed["added"] == [
        f"docs/engineering_controls/{day}/crypto-trials.harness_attestation.json",
        f"docs/engineering_controls/{day}/crypto-trials.phase1_harness_attestation.json",
    ]
    aligned = renewal._aligned(registry)
    assert [item["evidence_path"] for item in aligned] == changed["added"]
    for item in registry["harnesses"]:
        assert drift.check_recorded_evidence(item, root=root) == []
        assert drift.check_expiry(item, now) == []
    superseded = [item for item in registry["harnesses"] if item["status"] == "SUPERSEDED"]
    assert superseded and all(item["reissue_required"] is False for item in superseded)
    assert registry["last_verified_at"] == now.date().isoformat()
    assert renewal.apply(root, registry, CONFIG, now, folder) == {
        "expired": [],
        "superseded": [],
        "added": [],
    }


def test_apply_refuses_an_attestation_of_another_commit(root: Path) -> None:
    registry = _registry(root)
    now = _latest_aligned_expiry(registry) - renewal.timedelta(hours=24)
    folder = root / "staged"
    _write_attestations(folder, "2026-10-04T00:00:00Z", "2026-10-11T00:00:00Z", commit="f" * 40)
    with pytest.raises(SystemExit, match="code_version"):
        renewal.apply(root, registry, CONFIG, now, folder)


def test_without_a_reissue_an_expired_alignment_becomes_expired(root: Path) -> None:
    registry = _registry(root)
    now = _latest_aligned_expiry(registry) + renewal.timedelta(hours=1)
    changed = renewal.apply(root, registry, CONFIG, now, None)
    assert changed["expired"] and not changed["added"]
    assert renewal._aligned(registry) == []
    assert all(drift.check_expiry(item, now) == [] for item in registry["harnesses"])
    for item in registry["harnesses"]:
        if item.get("evidence_path") in changed["expired"]:
            assert item["status"] == "EXPIRED" and item["reissue_required"] is True


def test_cli_decide_writes_github_output(root: Path, tmp_path: Path, monkeypatch) -> None:
    output = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(output))
    now = _latest_aligned_expiry(_registry(root)) + renewal.timedelta(hours=1)
    assert renewal.main(["decide", "--root", str(root), "--now", now.isoformat()]) == 0
    assert output.read_text(encoding="utf-8").splitlines() == ["renew=true", "expired=true"]
