"""Falha quando o que os registries afirmam deixa de bater com os seis repositórios.

Existe porque a conferência manual envelhece: em 2026-09-06 o estado canônico estava
verificado havia três dias e já descrevia errado a versão de dois pacotes, o atestado
de um domínio e o status de pesquisa de um projeto. Três dias bastaram.

Dois modos:

    --offline-check   invariantes internas dos registries; sem rede.
    (padrão)          compara os registries contra o `main` real dos seis repos.

Cada checagem abaixo corresponde a uma divergência que já aconteceu de verdade.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import tomllib
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OWNER = "leonardosovienski"
REGISTRIES = ROOT / "registries"

# Onde cada domínio guarda o atestado de poder vigente.
ATTESTATIONS = {
    "brasileirao-predictor": "data/trials.harness_attestation.json",
    "cripto-predictor": "GarimpoInvestimentos/trials.harness_attestation.json",
    "stocks-predictor": "trials.harness_attestation.json",
}

# Todo lugar que carrega um pin de Core/Ops, por repositório. Nenhum deriva do outro:
# trocar só o pyproject passa na suíte local e quebra o CI. Aprendido em 2026-09-06,
# ao custo de três rodadas de CI vermelho.
PIN_FILES = {
    "brasileirao-predictor": ("pyproject.toml", "uv.lock"),
    "cripto-predictor": (
        "pyproject.toml",
        "uv.lock",
        "Dockerfile",
        ".github/workflows/ci.yml",
        "scripts/verify_installed_wheels.py",
        "tests/test_core_integrity.py",
    ),
    "stocks-predictor": ("pyproject.toml", "uv.lock", ".github/workflows/ci.yml"),
    "ecosystem-predictor": (".github/workflows/ci.yml",),
}
WHEEL_RE_CORE = "predictor_core-"
WHEEL_RE_OPS = "predictor_ops-"


class DriftError(RuntimeError):
    """Falha estável, usada pelo CI e pela reconciliação manual."""


class Source:
    """De onde vem a verdade de campo. Injetável para que a lógica seja testável.

    A implementação padrão lê o `main` no GitHub; `LocalSource` lê clones no disco.
    Sem isto a única forma de exercitar os detectores seria com rede.
    """

    def file(self, repo: str, path: str) -> str | None:
        raise NotImplementedError

    def main_sha(self, repo: str) -> str | None:
        raise NotImplementedError


class LocalSource(Source):
    """Lê `origin/main` de clones locais — usado em teste e na conferência manual."""

    def __init__(self, root: Path, ref: str = "origin/main") -> None:
        self.root = root
        self.ref = ref

    def _git(self, repo: str, *args: str) -> str | None:
        import subprocess  # noqa: PLC0415 - só o caminho local precisa

        path = self.root / repo
        if not path.exists():
            return None
        result = subprocess.run(  # noqa: S603 - args fixos
            ["git", "-C", str(path), *args], capture_output=True, text=True, check=False
        )
        return result.stdout if result.returncode == 0 else None

    def file(self, repo: str, path: str) -> str | None:
        return self._git(repo, "show", f"{self.ref}:{path}")

    def main_sha(self, repo: str) -> str | None:
        out = self._git(repo, "rev-parse", self.ref)
        return out.strip() if out else None


class GitHubSource(Source):
    """Lê o `main` publicado, pela API do GitHub."""

    def __init__(self, token: str | None = None, timeout: float = 30) -> None:
        self.token = token
        self.timeout = timeout

    def file(self, repo: str, path: str) -> str | None:
        try:
            payload = _request(f"/repos/{OWNER}/{repo}/contents/{path}", self.token, self.timeout)
        except DriftError:
            return None
        content = payload.get("content") if isinstance(payload, dict) else None
        if not isinstance(content, str):
            return None
        return base64.b64decode(content).decode("utf-8", errors="replace")

    def main_sha(self, repo: str) -> str | None:
        payload = _request(f"/repos/{OWNER}/{repo}/commits/main", self.token, self.timeout)
        sha = payload.get("sha") if isinstance(payload, dict) else None
        return sha if isinstance(sha, str) else None


def _load(name: str) -> dict[str, Any]:
    return json.loads((REGISTRIES / name).read_text(encoding="utf-8"))


def _request(path: str, token: str | None, timeout: float) -> Any:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ecosystem-drift/1"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com{path}", headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:  # noqa: S310 - host fixo
            return json.load(response)
    except (HTTPError, URLError, OSError, TimeoutError, json.JSONDecodeError) as exc:
        raise DriftError(f"SOURCE_UNAVAILABLE: {path}: {exc}") from exc


def wheel_versions(text: str) -> tuple[set[str], set[str]]:
    """Versões de wheel de Core e Ops citadas num arquivo, venham de onde vierem."""
    core: set[str] = set()
    ops: set[str] = set()
    for marker, bucket in ((WHEEL_RE_CORE, core), (WHEEL_RE_OPS, ops)):
        start = 0
        while (index := text.find(marker, start)) != -1:
            tail = text[index + len(marker) : index + len(marker) + 20]
            version = tail.split("-", 1)[0]
            if version and version[0].isdigit():
                bucket.add(version)
            start = index + len(marker)
    return core, ops


# --------------------------------------------------------------------------- offline


def check_recorded_evidence(item: dict[str, Any], root: Path = ROOT) -> list[str]:
    """Bind newly recorded controls to their original, hash-identified evidence."""
    if "evidence_path" not in item:
        return []
    try:
        relative = Path(item["evidence_path"])
        path = (root / relative).resolve()
        if relative.is_absolute() or not path.is_relative_to(root.resolve()):
            raise ValueError("evidence outside registry root")
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != item.get("evidence_sha256"):
            raise ValueError("evidence hash mismatch")
        evidence = json.loads(raw)
        fields = {
            "harness_version": "schema_version",
            "reported_core_version": "core_version",
            "domain_code_version": "code_version",
            "executed_at": "passed_at",
            "expires_at": "expires_at",
            "metric": "metric",
            "pipeline_fingerprint": "pipeline_fingerprint",
        }
        if any(
            not evidence.get(source) or item.get(target) != evidence[source]
            for target, source in fields.items()
        ):
            raise ValueError("registry fields differ from recorded evidence")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        return [f"{item['repo']}: recorded harness evidence invalid: {exc}"]
    return []


def check_offline() -> list[str]:
    """Invariantes que não dependem de rede — coerência interna dos registries."""
    problems: list[str] = []
    harness = _load("harness_registry.json")
    projects = {item["project_id"]: item for item in _load("project_registry.json")["projects"]}
    entries = harness["harnesses"]

    # 1. Atestado invalidado nunca pode dizer que não precisa reemitir.
    #    O registro do stocks dizia exatamente isso, com a justificativa
    #    "research is frozen" — e a pesquisa não estava congelada.
    for item in entries:
        problems.extend(check_recorded_evidence(item))
        if item["status"] == "INVALIDATED_BY_CORE_BUMP" and not item.get("reissue_required"):
            problems.append(f"{item['repo']}: atestado invalidado com reissue_required=false")
        if item.get("reported_core_version") == "UNKNOWN":
            problems.append(f"{item['repo']}: harness sem versão de Core declarada")

    # 2. A release anunciada como corrente tem que ser certificada por algum harness.
    #    Sem isto, o registry anunciou 3.1.0 por três dias depois do 3.2.0 sair.
    released = harness["current_released_core_version"]
    aligned = {item["reported_core_version"] for item in entries if item["status"] == "ALIGNED"}
    if not aligned:
        problems.append("nenhum harness ALIGNED: o ecossistema não tem certificação corrente")
    elif released not in aligned:
        problems.append(f"release corrente {released} não é certificada por nenhum harness ALIGNED")

    # 3. Atestado vencido não pode continuar ALIGNED.
    today = datetime.now(UTC).date()
    for item in entries:
        expires = item.get("expires_at")
        if not isinstance(expires, str) or expires == "UNKNOWN":
            continue
        when = date.fromisoformat(expires[:10])
        if when < today and item["status"] == "ALIGNED":
            problems.append(f"{item['repo']}: atestado venceu em {expires} e segue ALIGNED")

    # 4. Todo bloqueador citado por um projeto existe em PENDENCIAS_ABERTAS.md.
    pendencias = (ROOT / "PENDENCIAS_ABERTAS.md").read_text(encoding="utf-8")
    for project_id, project in projects.items():
        for blocker in project.get("open_blockers", []):
            if f"| {blocker} |" not in pendencias:
                problems.append(f"{project_id}: bloqueador {blocker} não está em PENDENCIAS_ABERTAS.md")

    # 5. Um repo com harness a reemitir tem que declarar isso como bloqueador.
    for item in entries:
        if item.get("reissue_required") and not projects.get(item["repo"], {}).get("open_blockers"):
            problems.append(f"{item['repo']}: harness exige reemissão mas o projeto não tem bloqueador")
    return problems


# ---------------------------------------------------------------------------- online


def check_online(source: Source) -> tuple[list[str], list[str]]:
    """Compara o que os registries afirmam com o `main` real de cada repositório.

    Devolve (problemas, avisos). A separação é deliberada: versão, pin e atestado
    divergentes SÃO falha — é o que esta checagem existe para pegar. SHA de `main`
    apenas se moveu, o que acontece a cada merge legítimo em qualquer repo; virar
    build vermelho por isso treinaria todo mundo a ignorar o vermelho.
    """
    problems: list[str] = []
    notes: list[str] = []
    projects = {item["project_id"]: item for item in _load("project_registry.json")["projects"]}
    harness = _load("harness_registry.json")

    versions: dict[str, str] = {}
    for repo in ("core-predictor", "predictor-ops"):
        content = source.file(repo, "pyproject.toml")
        if content is None:
            problems.append(f"{repo}: pyproject.toml ilegível em main")
            continue
        real = str(tomllib.loads(content).get("project", {}).get("version", ""))
        versions[repo] = real
        declared = projects.get(repo, {}).get("current_version")
        if declared != real:
            problems.append(f"{repo}: registry diz {declared}, main diz {real}")

    # A release corrente do Core tem que ser a versão do próprio core-predictor.
    if (core_real := versions.get("core-predictor")) and harness[
        "current_released_core_version"
    ] != core_real:
        problems.append(
            f"harness_registry.current_released_core_version="
            f"{harness['current_released_core_version']}, core-predictor main={core_real}"
        )

    # SHA de main: se divergiu, a verificação registrada é de outro estado.
    for repo, project in projects.items():
        recorded = project.get("remote_main_sha")
        if not recorded:
            continue
        real_sha = source.main_sha(repo)
        if isinstance(real_sha, str) and real_sha != recorded:
            notes.append(f"{repo}: registry aponta {recorded[:12]}, main está em {real_sha[:12]}")

    # Atestados: o arquivo real manda sobre o registro.
    by_repo: dict[str, list[dict[str, Any]]] = {}
    for item in harness["harnesses"]:
        by_repo.setdefault(item["repo"], []).append(item)
    for repo, path in ATTESTATIONS.items():
        raw = source.file(repo, path)
        if raw is None:
            problems.append(f"{repo}: atestado não encontrado em {path}")
            continue
        real = json.loads(raw)
        recorded = by_repo.get(repo, [])
        if not recorded:
            problems.append(f"{repo}: tem atestado no repo e nenhuma entrada no harness_registry")
            continue
        if not any(item["reported_core_version"] == real.get("core_version") for item in recorded):
            problems.append(
                f"{repo}: atestado real diz core {real.get('core_version')}, "
                f"registry diz {[item['reported_core_version'] for item in recorded]}"
            )
        if not any(item.get("expires_at") == real.get("expires_at") for item in recorded):
            problems.append(f"{repo}: expires_at do atestado real não bate com o registry")

    # Pins internos: cada repo tem que citar UMA versão de Core e UMA de Ops.
    # É a checagem que faltava — trocar só o pyproject não quebra a suíte local.
    for repo, paths in PIN_FILES.items():
        core_seen: dict[str, list[str]] = {}
        ops_seen: dict[str, list[str]] = {}
        for path in paths:
            content = source.file(repo, path)
            if content is None:
                continue
            core, ops = wheel_versions(content)
            for version in core:
                core_seen.setdefault(version, []).append(path)
            for version in ops:
                ops_seen.setdefault(version, []).append(path)
        for package, seen in (("Core", core_seen), ("Ops", ops_seen)):
            if len(seen) > 1:
                detail = "; ".join(f"{v} em {', '.join(sorted(f))}" for v, f in sorted(seen.items()))
                problems.append(f"{repo}: pin de {package} divergente entre arquivos — {detail}")
    return problems, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline-check", action="store_true", help="só invariantes internas")
    parser.add_argument("--token", default=None, help="token do GitHub (opcional)")
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument(
        "--from-clones",
        default=None,
        help="conferir a partir de clones locais em vez da API (ex.: /home/user)",
    )
    args = parser.parse_args()

    problems = check_offline()
    notes: list[str] = []
    scope = "OFFLINE"
    if not args.offline_check:
        scope = "OFFLINE+ONLINE"
        source: Source = (
            LocalSource(Path(args.from_clones))
            if args.from_clones
            else GitHubSource(args.token, args.timeout)
        )
        try:
            online, notes = check_online(source)
        except DriftError as exc:
            print(f"ECOSYSTEM_DRIFT_UNVERIFIABLE: {exc}")
            return 2
        problems += online

    for note in notes:
        print(f"  aviso: {note}")
    if problems:
        print(f"ECOSYSTEM_DRIFT_DETECTED ({scope}): {len(problems)}")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"ECOSYSTEM_NO_DRIFT ({scope})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
