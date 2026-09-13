"""Check documented components at one observed main SHA per repository.

This is a representation check, not compatibility or scientific certification.
It never updates release pins, receipts, or scientific states.
"""

import argparse
import base64
import json
import os
import subprocess
import tomllib
from datetime import UTC, datetime
from pathlib import Path

from check_ecosystem_drift import _request

ROOT = Path(__file__).resolve().parents[1]


def check_components(project, files):
    representation = project.get("representation", {})
    required = representation.get("source_paths", [])
    if not required or not representation.get("capabilities"):
        raise ValueError(f"{project['repository']}: representation missing")
    missing = set(required) - set(files)
    if missing:
        raise ValueError(f"{project['repository']}: documented components missing: {sorted(missing)}")
    actual = {
        p
        for p in files
        if p == "pyproject.toml" or p.startswith("packages/") and p.endswith("/pyproject.toml")
    }
    expected = {"pyproject.toml" if p == "." else p + "/pyproject.toml" for p in project["packages"]}
    if actual != expected:
        raise ValueError(f"{project['repository']}: package inventory changed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    registry = json.loads((ROOT / "registries/architecture_registry.json").read_text(encoding="utf-8"))
    results = []
    for project in registry["projects"]:
        name = project["repository"]
        rep = project["representation"]
        if not (ROOT / rep["ecosystem_document"]).is_file():
            raise ValueError(f"{name}: local project document missing")
        if args.offline and name != "ecosystem-predictor":
            if not rep["source_paths"] or not rep["capabilities"]:
                raise ValueError(f"{name}: empty representation")
            results.append({"repository": name, "remote_status": "NOT_CHECKED_OFFLINE"})
            continue
        if name == "ecosystem-predictor":
            files = subprocess.check_output(
                ["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT, text=True
            ).splitlines()
            sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
            raw = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        else:
            prefix = f"/repos/leonardosovienski/{name}"
            token = os.environ.get("GITHUB_TOKEN")
            sha = _request(prefix + "/commits/main", token, 30)["sha"]
            tree = _request(prefix + f"/git/trees/{sha}?recursive=1", token, 30)
            if tree.get("truncated"):
                raise ValueError(f"{name}: incomplete remote tree")
            files = [p["path"] for p in tree["tree"] if p["type"] == "blob"]
            manifest = _request(prefix + f"/contents/pyproject.toml?ref={sha}", token, 30)
            raw = base64.b64decode(manifest["content"]).decode("utf-8")
        check_components(project, files)
        results.append(
            {
                "repository": name,
                "observed_sha": sha,
                "version": tomllib.loads(raw)["project"]["version"],
                "status": "DOCUMENTED_PATHS_PRESENT",
                "source_scope": "working_tree" if name == "ecosystem-predictor" else "remote_main",
            }
        )
    result = {
        "observed_at": datetime.now(UTC).isoformat(),
        "projects": results,
        "limits": "Path/package presence only; no proof of runtime, full semantic coverage or science.",
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
