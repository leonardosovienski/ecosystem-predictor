"""Controle positivo do detector de drift.

Um detector que só foi visto passando não prova nada: é o mesmo argumento do
`testing.harness` do Core, que exige detectar edge plantado antes de aceitar um
NO-GO. Cada teste aqui planta uma divergência que JÁ ACONTECEU de verdade em
2026-09-06 e exige que o detector a encontre.
"""

import importlib.util
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_ecosystem_drift.py"
_SPEC = importlib.util.spec_from_file_location("ecosystem_drift_check", _SCRIPT)
assert _SPEC is not None and _SPEC.loader is not None
drift = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(drift)


class FakeSource(drift.Source):
    """Fonte de campo controlada: só o que o teste planta."""

    def __init__(self, files: dict[tuple[str, str], str], shas: dict[str, str] | None = None) -> None:
        self.files = files
        self.shas = shas or {}

    def file(self, repo: str, path: str) -> str | None:
        return self.files.get((repo, path))

    def main_sha(self, repo: str) -> str | None:
        return self.shas.get(repo)


def _pyproject(version: str) -> str:
    return f'[project]\nname = "x"\nversion = "{version}"\n'


def _fired(problems: list[str], needle: str) -> bool:
    return any(needle in problem for problem in problems)


# --------------------------------------------------------------- controles positivos


def test_detects_core_version_behind_the_registry(monkeypatch: pytest.MonkeyPatch) -> None:
    """O caso real: registry dizia 3.1.0 enquanto o core-predictor já estava em 3.2.0."""
    monkeypatch.setattr(
        drift,
        "_load",
        lambda name: {
            "project_registry.json": {
                "projects": [{"project_id": "core-predictor", "current_version": "3.1.0"}]
            },
            "harness_registry.json": {"current_released_core_version": "3.1.0", "harnesses": []},
        }[name],
    )
    problems, _ = drift.check_online(FakeSource({("core-predictor", "pyproject.toml"): _pyproject("3.2.0")}))
    assert _fired(problems, "core-predictor: registry diz 3.1.0, main diz 3.2.0")
    assert _fired(problems, "current_released_core_version")


def test_detects_attestation_that_the_registry_describes_wrong(monkeypatch: pytest.MonkeyPatch) -> None:
    """O caso real: o registry descrevia o atestado do stocks como legacy/UNKNOWN/STALE."""
    monkeypatch.setattr(
        drift,
        "_load",
        lambda name: {
            "project_registry.json": {"projects": []},
            "harness_registry.json": {
                "current_released_core_version": "3.2.0",
                "harnesses": [
                    {
                        "repo": "stocks-predictor",
                        "reported_core_version": "UNKNOWN",
                        "expires_at": "UNKNOWN",
                        "status": "STALE",
                    }
                ],
            },
        }[name],
    )
    real = '{"core_version": "3.1.0", "expires_at": "2026-09-11T08:48:24Z"}'
    problems, _ = drift.check_online(
        FakeSource({("stocks-predictor", "trials.harness_attestation.json"): real})
    )
    assert _fired(problems, "atestado real diz core 3.1.0")
    assert _fired(problems, "expires_at do atestado real não bate")


def test_detects_a_pin_changed_in_one_file_only(monkeypatch: pytest.MonkeyPatch) -> None:
    """O caso real, três vezes: trocar o pyproject e esquecer Dockerfile/workflow.

    A suíte local passa e o CI quebra com ResolutionImpossible.
    """
    monkeypatch.setattr(
        drift,
        "_load",
        lambda name: {
            "project_registry.json": {"projects": []},
            "harness_registry.json": {"current_released_core_version": "3.2.0", "harnesses": []},
        }[name],
    )
    source = FakeSource(
        {
            ("cripto-predictor", "pyproject.toml"): "predictor_ops-4.1.0-py3-none-any.whl",
            ("cripto-predictor", "Dockerfile"): "predictor_ops-4.0.0-py3-none-any.whl",
        }
    )
    problems, _ = drift.check_online(source)
    assert _fired(problems, "pin de Ops divergente")
    assert _fired(problems, "Dockerfile")


def test_detects_main_that_moved_past_the_recorded_verification(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        drift,
        "_load",
        lambda name: {
            "project_registry.json": {
                "projects": [{"project_id": "stocks-predictor", "remote_main_sha": "a" * 40}]
            },
            "harness_registry.json": {"current_released_core_version": "3.2.0", "harnesses": []},
        }[name],
    )
    problems, notes = drift.check_online(FakeSource({}, {"stocks-predictor": "b" * 40}))
    assert _fired(notes, "registry aponta aaaaaaaaaaaa, main está em bbbbbbbbbbbb")
    assert not _fired(problems, "main está em"), (
        "SHA movido é aviso, não falha: acontece a cada merge legítimo em qualquer repo"
    )


def test_wheel_versions_reads_every_shape_a_pin_takes() -> None:
    core, ops = drift.wheel_versions(
        'url = "https://x/download/v3.2.0/predictor_core-3.2.0-py3-none-any.whl"\n'
        '"predictor-ops @ https://x/predictor_ops-4.1.0-py3-none-any.whl"\n'
    )
    assert core == {"3.2.0"}
    assert ops == {"4.1.0"}


# ------------------------------------------------------------- controle de ruído


def test_agreeing_pins_do_not_fire(monkeypatch: pytest.MonkeyPatch) -> None:
    """Especificidade: sem divergência plantada, o detector fica calado."""
    monkeypatch.setattr(
        drift,
        "_load",
        lambda name: {
            "project_registry.json": {"projects": []},
            "harness_registry.json": {"current_released_core_version": "3.2.0", "harnesses": []},
        }[name],
    )
    same = "predictor_core-3.2.0-py3-none-any.whl"
    source = FakeSource(
        {
            ("stocks-predictor", "pyproject.toml"): same,
            ("stocks-predictor", "uv.lock"): same,
            ("stocks-predictor", ".github/workflows/ci.yml"): same,
        }
    )
    problems, _ = drift.check_online(source)
    assert not [p for p in problems if "pin de" in p]


def test_the_real_registries_pass_their_own_offline_invariants() -> None:
    assert drift.check_offline() == []
