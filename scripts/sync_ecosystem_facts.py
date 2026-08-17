"""Generate and validate the read-only mechanical ecosystem inventory."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import tomllib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OWNER = "leonardosovienski"
SCHEMA = "ecosystem-facts/1"
REPOSITORIES = (
    "ecosystem-predictor",
    "core-predictor",
    "predictor-ops",
    "brasileirao-predictor",
    "cripto-predictor",
    "cs-predictor",
    "f1-predictor",
    "lol-predictor",
    "wc-predictor",
)
CANONICAL_NAMES = {
    "README.md",
    "HANDOFF.md",
    "ECOSYSTEM_HANDOFF.md",
    "ECOSYSTEM_CURRENT_STATE.md",
    "P4_CONSOLIDATION.md",
    "pyproject.toml",
    "requirements.txt",
    "uv.lock",
}
MECHANICAL_FIELDS = (
    "repository",
    "branch",
    "head",
    "source_ref",
    "version",
    "python",
    "core",
    "ops",
    "workflow",
    "ci",
    "ci_url",
    "canonical",
)
START = "<!-- mechanical-facts:start -->"
END = "<!-- mechanical-facts:end -->"


class FactError(RuntimeError):
    """A fact operation failed with a stable, machine-readable classification."""

    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"{code}: {message}")


def _request(path: str, token: str | None, *, timeout: float = 30) -> Any:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ecosystem-facts/1"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com{path}", headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed host
            return json.load(response)
    except (HTTPError, URLError, OSError, TimeoutError, json.JSONDecodeError) as exc:
        raise FactError("SOURCE_UNAVAILABLE", f"GitHub request failed for {path}: {exc}") from exc


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


def _package_facts(content: str | None) -> tuple[str, str, str, str]:
    if content is None:
        return "requirements", "não declarado", "legado vendorizado", "—"
    try:
        document = tomllib.loads(content)
    except tomllib.TOMLDecodeError as exc:
        raise FactError("INVALID_SCHEMA", f"invalid pyproject.toml: {exc}") from exc
    project = document.get("project", {})
    core = _dependency(project, "predictor-core")
    ops = _dependency(project, "predictor-ops")
    core_tag = _source_tag(document, "predictor-core")
    ops_tag = _source_tag(document, "predictor-ops")
    if core_tag:
        core = f"{core} ({core_tag})"
    if ops_tag:
        ops = f"{ops} ({ops_tag})"
    return (
        str(project.get("version", "—")),
        str(project.get("requires-python", "—")),
        core,
        ops,
    )


def collect(token: str | None = None, *, timeout: float = 30) -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = []
    for repository in REPOSITORIES:
        metadata = _request(f"/repos/{OWNER}/{repository}", token, timeout=timeout)
        branch = metadata["default_branch"]
        commit = _request(f"/repos/{OWNER}/{repository}/commits/{branch}", token, timeout=timeout)["sha"]
        tree = _request(
            f"/repos/{OWNER}/{repository}/git/trees/{commit}?recursive=1",
            token,
            timeout=timeout,
        )["tree"]
        paths = {item["path"] for item in tree if item.get("type") == "blob"}
        canonical = sorted(path for path in paths if "/" not in path and Path(path).name in CANONICAL_NAMES)
        pyproject: str | None = None
        if "pyproject.toml" in paths:
            encoded = _request(
                f"/repos/{OWNER}/{repository}/contents/pyproject.toml?ref={commit}",
                token,
                timeout=timeout,
            )["content"]
            pyproject = base64.b64decode(encoded).decode("utf-8")
        version, python, core, ops = _package_facts(pyproject)

        workflow = ".github/workflows/ci.yml" if ".github/workflows/ci.yml" in paths else "—"
        runs = _request(
            f"/repos/{OWNER}/{repository}/actions/runs?branch={branch}&per_page=50",
            token,
            timeout=timeout,
        ).get("workflow_runs", [])
        matching = [run for run in runs if run.get("head_sha") == commit]
        successful = next(
            (run for run in matching if run.get("conclusion") == "success" and run.get("path") == workflow),
            None,
        )
        ci = "NOT_APPLICABLE" if workflow == "—" else "UNKNOWN"
        ci_url = ""
        if successful:
            ci, ci_url = "success", successful["html_url"]
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
                "workflow": workflow,
                "ci": ci,
                "ci_url": ci_url,
                "canonical": canonical,
            }
        )
    return facts


def make_snapshot(facts: list[dict[str, Any]], generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA,
        "generated_at": generated_at,
        "source_ref": "runtime checkout (self HEAD derived, never pinned)",
        "human_decision_policy": "HUMAN_DECISION_UNTOUCHED",
        "repositories": sorted(facts, key=lambda item: item["repository"]),
    }


def validate_schema(snapshot: dict[str, Any]) -> None:
    if (
        set(snapshot)
        != {
            "schema_version",
            "generated_at",
            "source_ref",
            "human_decision_policy",
            "repositories",
        }
        or snapshot.get("schema_version") != SCHEMA
    ):
        raise FactError("INVALID_SCHEMA", "snapshot top-level fields are invalid")
    repositories = snapshot.get("repositories")
    if not isinstance(repositories, list):
        raise FactError("INVALID_SCHEMA", "repositories must be a list")
    names: list[str] = []
    for fact in repositories:
        if not isinstance(fact, dict) or set(fact) != set(MECHANICAL_FIELDS):
            raise FactError("INVALID_SCHEMA", "repository fields are invalid")
        if not isinstance(fact["canonical"], list):
            raise FactError("INVALID_SCHEMA", "canonical must be a list")
        names.append(fact["repository"])
    if names != sorted(names) or len(names) != len(set(names)):
        raise FactError("INVALID_SCHEMA", "repositories must be unique and sorted")


def compare(expected: dict[str, Any], observed: dict[str, Any]) -> None:
    validate_schema(expected)
    validate_schema(observed)
    old = {item["repository"]: item for item in expected["repositories"]}
    new = {item["repository"]: item for item in observed["repositories"]}
    if old.keys() != new.keys():
        raise FactError("FACTUAL_DRIFT", "repository set changed")
    differences: list[str] = []
    for repository in sorted(old):
        for field in MECHANICAL_FIELDS:
            if repository == "ecosystem-predictor" and field in {
                "head",
                "source_ref",
                "ci",
                "ci_url",
            }:
                continue
            if old[repository][field] != new[repository][field]:
                differences.append(f"{repository}.{field}")
    if differences:
        raise FactError("FACTUAL_DRIFT", ", ".join(differences))


def validate_links(document: Path) -> None:
    missing: list[str] = []
    for path in (document, document.with_name("README.md")):
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            local = path.parent / target.split("#", 1)[0]
            if not local.exists():
                missing.append(f"{path.name}:{target}")
    if missing:
        raise FactError("FACTUAL_DRIFT", "broken internal links: " + ", ".join(missing))


def validate_freshness(snapshot: dict[str, Any], *, now: datetime, max_age_hours: float) -> None:
    try:
        generated_at = datetime.fromisoformat(snapshot["generated_at"].replace("Z", "+00:00"))
    except (KeyError, TypeError, ValueError) as exc:
        raise FactError("INVALID_SCHEMA", "generated_at is invalid") from exc
    age_hours = (now.astimezone(UTC) - generated_at.astimezone(UTC)).total_seconds() / 3600
    if age_hours > max_age_hours:
        raise FactError(
            "STALE_REVIEW_REQUIRED",
            f"snapshot age {age_hours:.1f}h exceeds {max_age_hours:.1f}h",
        )


def render(snapshot: dict[str, Any]) -> str:
    validate_schema(snapshot)
    lines = [
        START,
        f"_Snapshot mecânico `{snapshot['schema_version']}`; gerado em `{snapshot['generated_at']}`._",
        "_Decisões humanas são preservadas e ignoradas pelo validador._",
        "",
        "| Repositório | Branch / HEAD | Pacote / Python | Core / Ops | CI | Canônicos |",
        "|---|---|---|---|---|---|",
    ]
    for fact in snapshot["repositories"]:
        ci = fact["ci"]
        head = f"`{fact['head'][:12]}`"
        if fact["repository"] == "ecosystem-predictor":
            head, ci = "HEAD derivado em execução", "workflow atual"
        elif fact.get("ci_url"):
            ci = f"[{ci}]({fact['ci_url']})"
        canonical = ", ".join(f"`{path}`" for path in fact["canonical"]) or "—"
        lines.append(
            f"| `{fact['repository']}` | `{fact['branch']}` / {head} | "
            f"`{fact['version']}` / `{fact['python']}` | Core `{fact['core']}` / Ops `{fact['ops']}` | "
            f"{ci} | {canonical} |"
        )
    lines.extend([END, ""])
    return "\n".join(lines)


def update_document(document: str, block: str) -> str:
    if START in document and END in document:
        before, rest = document.split(START, 1)
        _, after = rest.split(END, 1)
        return before + block.rstrip() + after
    raise FactError("INVALID_SCHEMA", "generated inventory markers not found")


def _load(path: Path) -> dict[str, Any]:
    try:
        snapshot = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FactError("INVALID_SCHEMA", f"cannot read snapshot: {exc}") from exc
    validate_schema(snapshot)
    return snapshot


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="remote drift check; never writes")
    mode.add_argument("--offline-check", action="store_true", help="schema/docs check; no network")
    mode.add_argument("--write", action="store_true", help="explicitly refresh snapshot and document")
    parser.add_argument("--snapshot", type=Path, default=Path("audit/ecosystem-facts.json"))
    parser.add_argument("--document", type=Path, default=Path("ECOSYSTEM_CURRENT_STATE.md"))
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--max-age-hours", type=float, default=168)
    parser.add_argument("--generated-at")
    args = parser.parse_args(argv)

    expected = _load(args.snapshot) if args.snapshot.exists() and not args.write else None
    if args.offline_check:
        if expected is None:
            raise FactError("INVALID_SCHEMA", "snapshot is absent")
        rendered = update_document(args.document.read_text(encoding="utf-8"), render(expected))
        if rendered != args.document.read_text(encoding="utf-8"):
            raise FactError("FACTUAL_DRIFT", "document differs from the deterministic snapshot")
        validate_links(args.document)
        print("HUMAN_DECISION_UNTOUCHED")
        return 0

    generated_at = args.generated_at or datetime.now(UTC).isoformat(timespec="seconds")
    observed = make_snapshot(collect(os.getenv("GITHUB_TOKEN"), timeout=args.timeout), generated_at)
    if args.check:
        if expected is None:
            raise FactError("INVALID_SCHEMA", "snapshot is absent")
        validate_freshness(expected, now=datetime.now(UTC), max_age_hours=args.max_age_hours)
        compare(expected, observed)
        validate_links(args.document)
        print("HUMAN_DECISION_UNTOUCHED")
        return 0

    args.snapshot.parent.mkdir(parents=True, exist_ok=True)
    args.snapshot.write_text(json.dumps(observed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    current = args.document.read_text(encoding="utf-8")
    args.document.write_text(update_document(current, render(observed)), encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
