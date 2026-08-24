"""Generate and validate the mechanical inventory of the six canonical repos."""

from __future__ import annotations

import argparse
import base64
import json
import os
import tomllib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OWNER = "leonardosovienski"
SCHEMA = "canonical-ecosystem-facts/2"
REPOSITORIES = (
    "ecosystem-predictor",
    "core-predictor",
    "predictor-ops",
    "cripto-predictor",
    "brasileirao-predictor",
    "stocks-predictor",
)
CANONICAL_NAMES = {
    "README.md",
    "HANDOFF.md",
    "STOCKS_CURRENT_STATE.md",
    "ECOSYSTEM_CHARTER.md",
    "ECOSYSTEM_HANDOFF_2026-08-23.md",
    "ECOSYSTEM_MECHANICAL_STATE.md",
    "PREDICTOR_CONTRACT.md",
    "pyproject.toml",
    "requirements.txt",
    "uv.lock",
}
FIELDS = (
    "repository",
    "branch",
    "head",
    "source_ref",
    "version",
    "python",
    "core",
    "ops",
    "plugin",
    "workflow",
    "canonical",
)
SELF_DYNAMIC_FIELDS = {"head", "source_ref"}
START = "<!-- canonical-mechanical-facts:start -->"
END = "<!-- canonical-mechanical-facts:end -->"


class FactError(RuntimeError):
    """Stable failure used by CI and manual reconciliation."""


def _request(path: str, token: str | None, timeout: float) -> Any:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": SCHEMA}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com{path}", headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed host
            return json.load(response)
    except (HTTPError, URLError, OSError, TimeoutError, json.JSONDecodeError) as exc:
        raise FactError(f"SOURCE_UNAVAILABLE: {path}: {exc}") from exc


def _dependency(project: dict[str, Any], package: str) -> str:
    prefix = package.casefold()
    for dependency in project.get("dependencies", []):
        if dependency.casefold().startswith(prefix):
            return dependency[len(package) :].strip() or "declared"
    return "—"


def _source_tag(document: dict[str, Any], package: str) -> str:
    source = document.get("tool", {}).get("uv", {}).get("sources", {}).get(package, {})
    url = source.get("url") if isinstance(source, dict) else None
    if not url:
        return ""
    marker = "/download/"
    return url.split(marker, 1)[1].split("/", 1)[0] if marker in url else "URL"


def _plugin_fact(project: dict[str, Any]) -> str:
    entry_points = project.get("entry-points", {})
    plugins = entry_points.get("predictor.plugins", {}) if isinstance(entry_points, dict) else {}
    if not isinstance(plugins, dict) or not plugins:
        return "—"
    return ", ".join(f"{name}={target}" for name, target in sorted(plugins.items()))


def _package_facts(content: str | None) -> tuple[str, str, str, str, str]:
    if content is None:
        return "requirements", "não declarado", "legado vendorizado", "—", "—"
    document = tomllib.loads(content)
    project = document.get("project", {})
    core = _dependency(project, "predictor-core")
    ops = _dependency(project, "predictor-ops")
    if tag := _source_tag(document, "predictor-core"):
        core = f"{core} ({tag})"
    if tag := _source_tag(document, "predictor-ops"):
        ops = f"{ops} ({tag})"
    return (
        str(project.get("version", "—")),
        str(project.get("requires-python", "—")),
        core,
        ops,
        _plugin_fact(project),
    )


def collect(token: str | None = None, timeout: float = 30) -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = []
    for repository in REPOSITORIES:
        metadata = _request(f"/repos/{OWNER}/{repository}", token, timeout)
        branch = metadata["default_branch"]
        commit = _request(f"/repos/{OWNER}/{repository}/commits/{branch}", token, timeout)["sha"]
        tree = _request(f"/repos/{OWNER}/{repository}/git/trees/{commit}?recursive=1", token, timeout)["tree"]
        paths = {item["path"] for item in tree if item.get("type") == "blob"}
        canonical = sorted(path for path in paths if "/" not in path and Path(path).name in CANONICAL_NAMES)
        pyproject: str | None = None
        if "pyproject.toml" in paths:
            encoded = _request(
                f"/repos/{OWNER}/{repository}/contents/pyproject.toml?ref={commit}", token, timeout
            )["content"]
            pyproject = base64.b64decode(encoded).decode("utf-8")
        version, python, core, ops, plugin = _package_facts(pyproject)
        facts.append(
            {
                "repository": repository,
                "branch": branch,
                "head": commit,
                "source_ref": f"{repository}@{commit}",
                "version": version,
                "python": python,
                "core": core,
                "ops": ops,
                "plugin": plugin,
                "workflow": ".github/workflows/ci.yml" if ".github/workflows/ci.yml" in paths else "—",
                "canonical": canonical,
            }
        )
    return sorted(facts, key=lambda item: item["repository"])


def make_snapshot(facts: list[dict[str, Any]], generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA,
        "generated_at": generated_at,
        "scope_authority": "ECOSYSTEM_CHARTER.md",
        "repositories": facts,
    }


def validate(snapshot: dict[str, Any]) -> None:
    if set(snapshot) != {"schema_version", "generated_at", "scope_authority", "repositories"}:
        raise FactError("INVALID_SCHEMA: top-level fields")
    if snapshot["schema_version"] != SCHEMA or snapshot["scope_authority"] != "ECOSYSTEM_CHARTER.md":
        raise FactError("INVALID_SCHEMA: schema/authority")
    repositories = snapshot["repositories"]
    if not isinstance(repositories, list):
        raise FactError("INVALID_SCHEMA: repositories")
    names: list[str] = []
    for fact in repositories:
        if not isinstance(fact, dict) or set(fact) != set(FIELDS):
            raise FactError("INVALID_SCHEMA: repository fields")
        if not isinstance(fact["canonical"], list):
            raise FactError("INVALID_SCHEMA: canonical")
        names.append(fact["repository"])
    if names != sorted(REPOSITORIES):
        raise FactError(f"CANONICAL_SCOPE_DRIFT: expected {sorted(REPOSITORIES)}, got {names}")


def render(snapshot: dict[str, Any]) -> str:
    validate(snapshot)
    lines = [
        START,
        f"_Snapshot `{snapshot['schema_version']}` gerado em `{snapshot['generated_at']}`._",
        "_Escopo humano vem de `ECOSYSTEM_CHARTER.md`; este bloco só mede fatos mecânicos._",
        "",
        "| Repositório | Branch / HEAD | Pacote / Python | Core / Ops | Plugin | Workflow | Canônicos |",
        "|---|---|---|---|---|---|---|",
    ]
    for fact in snapshot["repositories"]:
        canonical = ", ".join(f"`{path}`" for path in fact["canonical"]) or "—"
        lines.append(
            f"| `{fact['repository']}` | `{fact['branch']}` / `{fact['head'][:12]}` | "
            f"`{fact['version']}` / `{fact['python']}` | Core `{fact['core']}` / Ops `{fact['ops']}` | "
            f"`{fact['plugin']}` | `{fact['workflow']}` | {canonical} |"
        )
    lines.extend([END, ""])
    return "\n".join(lines)


def update_document(document: str, block: str) -> str:
    if START not in document or END not in document:
        raise FactError("INVALID_SCHEMA: inventory markers not found")
    before, rest = document.split(START, 1)
    _, after = rest.split(END, 1)
    return before + block.rstrip() + after


def load(path: Path) -> dict[str, Any]:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    validate(snapshot)
    return snapshot


def compare(expected: dict[str, Any], observed: dict[str, Any]) -> None:
    validate(expected)
    validate(observed)
    old = {item["repository"]: item for item in expected["repositories"]}
    new = {item["repository"]: item for item in observed["repositories"]}
    differences: list[str] = []
    for repository in sorted(old):
        for field in FIELDS:
            if repository == "ecosystem-predictor" and field in SELF_DYNAMIC_FIELDS:
                continue
            if old[repository][field] != new[repository][field]:
                differences.append(f"{repository}.{field}")
    if differences:
        raise FactError("FACTUAL_DRIFT: " + ", ".join(differences))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--offline-check", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument("--snapshot", type=Path, default=Path("audit/canonical-ecosystem-facts.json"))
    parser.add_argument("--document", type=Path, default=Path("ECOSYSTEM_MECHANICAL_STATE.md"))
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--generated-at")
    args = parser.parse_args(argv)

    expected = load(args.snapshot) if args.snapshot.exists() else None
    if args.offline_check:
        if expected is None:
            raise FactError("INVALID_SCHEMA: snapshot absent")
        current = args.document.read_text(encoding="utf-8")
        if update_document(current, render(expected)) != current:
            raise FactError("FACTUAL_DRIFT: document differs from snapshot")
        print("CANONICAL_SCOPE_OK")
        return 0

    observed = make_snapshot(
        collect(os.getenv("GITHUB_TOKEN"), args.timeout),
        args.generated_at or datetime.now(UTC).isoformat(timespec="seconds"),
    )
    if args.check:
        if expected is None:
            raise FactError("INVALID_SCHEMA: snapshot absent")
        compare(expected, observed)
        print("CANONICAL_SCOPE_OK")
        return 0

    args.snapshot.parent.mkdir(parents=True, exist_ok=True)
    args.snapshot.write_text(json.dumps(observed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    current = args.document.read_text(encoding="utf-8")
    args.document.write_text(update_document(current, render(observed)), encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
