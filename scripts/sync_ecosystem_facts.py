"""Generate or validate the mechanical ecosystem inventory.

Only repository metadata is generated here. Scientific states, decisions and
interpretations remain human-authored outside the generated block.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import tomllib
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

OWNER = "leonardosovienski"
REPOSITORIES = (
    "ecosystem-predictor",
    "core-predictor",
    "tools-predictor",
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
START = "<!-- mechanical-facts:start -->"
END = "<!-- mechanical-facts:end -->"


class FactError(RuntimeError):
    """A remote fact could not be obtained or validated."""


def _request(path: str, token: str | None) -> Any:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ecosystem-facts/1"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com{path}", headers=headers)
    try:
        with urlopen(request, timeout=30) as response:  # noqa: S310 - fixed GitHub host
            return json.load(response)
    except (HTTPError, OSError, json.JSONDecodeError) as exc:
        raise FactError(f"GitHub request failed for {path}: {exc}") from exc


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
    document = tomllib.loads(content)
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


def collect(token: str | None = None) -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = []
    for repository in REPOSITORIES:
        metadata = _request(f"/repos/{OWNER}/{repository}", token)
        branch = metadata["default_branch"]
        commit = _request(f"/repos/{OWNER}/{repository}/commits/{branch}", token)["sha"]
        tree = _request(f"/repos/{OWNER}/{repository}/git/trees/{commit}?recursive=1", token)["tree"]
        paths = {item["path"] for item in tree if item.get("type") == "blob"}
        canonical = sorted(path for path in paths if "/" not in path and Path(path).name in CANONICAL_NAMES)

        pyproject: str | None = None
        if "pyproject.toml" in paths:
            encoded = _request(f"/repos/{OWNER}/{repository}/contents/pyproject.toml?ref={commit}", token)[
                "content"
            ]
            pyproject = base64.b64decode(encoded).decode("utf-8")
        version, python, core, ops = _package_facts(pyproject)

        runs = _request(f"/repos/{OWNER}/{repository}/actions/runs?branch={branch}&per_page=50", token).get(
            "workflow_runs", []
        )
        matching = [run for run in runs if run.get("head_sha") == commit]
        successful = next(
            (
                run
                for run in matching
                if run.get("conclusion") == "success" and run.get("path") == ".github/workflows/ci.yml"
            ),
            None,
        )
        ci = "NOT_APPLICABLE" if not matching and ".github/workflows/ci.yml" not in paths else "UNKNOWN"
        ci_url = ""
        if successful:
            ci = "success"
            ci_url = successful["html_url"]

        facts.append(
            {
                "repository": repository,
                "branch": branch,
                "head": commit,
                "version": version,
                "python": python,
                "core": core,
                "ops": ops,
                "ci": ci,
                "ci_url": ci_url,
                "canonical": canonical,
            }
        )
    return facts


def render(facts: list[dict[str, Any]]) -> str:
    lines = [
        START,
        "_Bloco mecânico gerado por `scripts/sync_ecosystem_facts.py`; decisões humanas não são geradas._",
        "",
        "| Repositório | Branch / HEAD | Pacote / Python | Core / Ops | CI | Canônicos |",
        "|---|---|---|---|---|---|",
    ]
    for fact in facts:
        ci = fact["ci"]
        head = f"`{fact['head'][:12]}`"
        if fact["repository"] == "ecosystem-predictor":
            # A committed document cannot contain its own final Git SHA: adding
            # that SHA changes the commit. Git identifies this file's revision,
            # while the active workflow validates it. Remote SHAs remain pinned
            # for every external repository.
            head = "commit deste documento"
            ci = "workflow atual"
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
    inventory = "## Inventário mecânico"
    evidence = "## Evidência por alegação"
    if inventory not in document or evidence not in document:
        raise FactError("inventory section boundaries not found")
    before, rest = document.split(inventory, 1)
    _, after = rest.split(evidence, 1)
    return f"{before}{inventory}\n\n{block}\n{evidence}{after}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--fixture", type=Path)
    parser.add_argument("--document", type=Path, default=Path("ECOSYSTEM_CURRENT_STATE.md"))
    args = parser.parse_args(argv)
    if args.check == args.write:
        parser.error("choose exactly one of --check or --write")

    facts = (
        json.loads(args.fixture.read_text(encoding="utf-8"))
        if args.fixture
        else collect(os.getenv("GITHUB_TOKEN"))
    )
    current = args.document.read_text(encoding="utf-8")
    expected = update_document(current, render(facts))
    if args.check:
        if current != expected:
            raise FactError("mechanical inventory is stale; run with --write")
        return 0
    args.document.write_text(expected, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
