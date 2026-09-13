"""Check topology against actual package metadata at explicit source revisions."""

import json
import os
import re
import subprocess
import tomllib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def package_paths(files):
    """Use the same package scope as inventory_packages, without a fixed count."""
    return {
        str(Path(name).parent).replace("\\", "/")
        for name in files
        if name == "pyproject.toml" or (name.startswith("packages/") and name.endswith("/pyproject.toml"))
    }


def validate_package_inventory(repository, declared, files):
    actual = package_paths(files)
    if len(declared) != len(set(declared)) or set(declared) != actual:
        raise ValueError(
            f"{repository}: package inventory differs: declared={sorted(declared)}, actual={sorted(actual)}"
        )
    if not actual:
        raise ValueError(f"{repository}: no package metadata found")
    return actual


def remote_files(repository, revision):
    """Read root and packages trees only, without fetching domain datasets."""

    def tree(ref, recursive=False):
        suffix = "?recursive=1" if recursive else ""
        url = f"https://api.github.com/repos/leonardosovienski/{repository}/git/trees/{ref}{suffix}"
        headers = {"User-Agent": "ecosystem-package-inventory"}
        if token := os.environ.get("GITHUB_TOKEN"):
            headers["Authorization"] = f"Bearer {token}"
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
            result = json.load(response)
        if result.get("truncated"):
            raise ValueError(f"{repository}: incomplete Git tree")
        return result["tree"]

    entries = tree(revision)
    files = [entry["path"] for entry in entries if entry["type"] == "blob"]
    for entry in entries:
        if entry["path"] == "packages" and entry["type"] == "tree":
            files.extend(
                "packages/" + item["path"]
                for item in tree(entry["sha"], recursive=True)
                if item["type"] == "blob"
            )
    return files


def main():
    topology = json.loads((ROOT / "registries/architecture_registry.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "registries/compatibility_candidate.json").read_text(encoding="utf-8"))
    releases = json.loads((ROOT / "registries/released_architecture.json").read_text(encoding="utf-8"))
    projects = topology["projects"]
    assert len(projects) == 7 and len({p["repository"] for p in projects}) == 7
    assert topology["shared_database"] is False and manifest["capital_authorized"] is False
    revisions = {item["repository"]: item["source_commit"] for item in releases["repositories"]}
    revisions.update({name: item["commit"] for name, item in manifest["consumers"].items()})
    count = 0
    for item in projects:
        repository = item["repository"]
        if repository == "ecosystem-predictor":
            files = subprocess.check_output(
                ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                cwd=ROOT,
                text=True,
                encoding="utf-8",
            ).splitlines()
        else:
            revision = revisions[repository]
            assert re.fullmatch(r"[0-9a-f]{40}", revision)
            files = remote_files(repository, revision)
        count += len(validate_package_inventory(repository, item["packages"], files))
    for name, item in manifest["consumers"].items():
        assert re.fullmatch(r"[0-9a-f]{40}", item["commit"])
        url = item["repository"].replace("https://github.com/", "https://raw.githubusercontent.com/")
        with urllib.request.urlopen(f"{url}/{item['commit']}/pyproject.toml", timeout=60) as response:
            project = tomllib.loads(response.read().decode())["project"]
        package_name = "cain-research" if name == "cain" else name
        assert (project["name"], project["version"]) == (package_name, item["version"])
    for item in manifest["shared"].values():
        assert re.fullmatch(r"sha256:[0-9a-f]{64}", item["hash"])
        assert f"/v{item['version']}/" in item["url"]
    print(f"seven repositories, {count} packages and immutable remote sources verified")


if __name__ == "__main__":
    main()
