"""Inventory explicit local candidates, including separately distributed subpackages.

No network, imports from consumers, databases or inferred compatibility claims.
Historical main snapshots remain separate from candidate source and wheel bytes.
"""

import argparse
import hashlib
import json
import subprocess
import tomllib
import zipfile
from email.parser import BytesParser
from pathlib import Path

REPOSITORIES = {
    "cripto-predictor",
    "stocks-predictor",
    "brasileirao-predictor",
    "core-predictor",
    "predictor-ops",
    "ecosystem-predictor",
    "cain",
}


def git(root: Path, *arguments: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *arguments], text=True, encoding="utf-8").strip()


def package(root: Path, relative: str) -> dict:
    raw = (root / relative).read_bytes()
    project = tomllib.loads(raw.decode("utf-8"))["project"]
    return {
        "path": str(Path(relative).parent).replace("\\", "/"),
        "name": project["name"],
        "version": project["version"],
        "requires_python": project.get("requires-python"),
        "dependencies": project.get("dependencies", []),
        "pyproject_sha256": hashlib.sha256(raw).hexdigest(),
    }


def inventory(checkouts: dict[str, Path], wheels: list[Path]) -> dict:
    if set(checkouts) != REPOSITORIES:
        raise ValueError("inventory requires exactly the seven explicit repositories")
    repositories = []
    for name, root in sorted(checkouts.items()):
        paths = set(git(root, "ls-files", "--cached", "--others", "--exclude-standard").splitlines())
        projects = sorted(
            path
            for path in paths
            if path == "pyproject.toml" or (path.startswith("packages/") and path.endswith("/pyproject.toml"))
        )
        if not projects:
            raise ValueError(f"missing package metadata: {name}")
        sources = {}
        for path in sorted(paths):
            if (path.endswith(".py") or path in projects) and not path.startswith(
                ("research/", "tests/", "tools/", "scripts/")
            ):
                file = root / path
                if file.is_file():
                    sources[path] = hashlib.sha256(file.read_bytes()).hexdigest()
        repositories.append(
            {
                "repository": name,
                "base_commit": git(root, "rev-parse", "HEAD"),
                "branch": git(root, "branch", "--show-current"),
                "dirty": bool(git(root, "status", "--porcelain")),
                "packages": [package(root, path) for path in projects],
                "source_files": sources,
            }
        )
    artifacts = []
    for wheel in sorted(wheels):
        with zipfile.ZipFile(wheel) as archive:
            members = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
            if len(members) != 1:
                raise ValueError("ambiguous wheel metadata")
            metadata = BytesParser().parsebytes(archive.read(members[0]))
        artifacts.append(
            {
                "filename": wheel.name,
                "sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(),
                "name": metadata["Name"],
                "version": metadata["Version"],
                "requires_python": metadata["Requires-Python"],
                "requires_dist": metadata.get_all("Requires-Dist", []),
            }
        )
    return {
        "schema_version": "architecture-candidates/1",
        "repositories": repositories,
        "wheels": artifacts,
        "compatibility": "UNVERIFIED_UNLESS_LINKED_TO_A_TEST_RECEIPT",
        "authority": "implementation requested after architecture review; no economic promotion",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", action="append", required=True, help="repository=path")
    parser.add_argument("--wheel", action="append", type=Path, default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    pairs = [value.split("=", 1) for value in args.checkout]
    if len({name for name, _ in pairs}) != len(pairs):
        raise ValueError("duplicate repository mapping")
    result = inventory({name: Path(path) for name, path in pairs}, args.wheel)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
