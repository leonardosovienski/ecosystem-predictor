"""Check the seven-project topology and immutable remote candidate identities."""

import json
import re
import tomllib
import urllib.request
from pathlib import Path


def main():
    topology = json.loads(Path("registries/architecture_registry.json").read_text())
    manifest = json.loads(Path("registries/compatibility_candidate.json").read_text())
    projects = topology["projects"]
    assert len(projects) == 7 and len({p["repository"] for p in projects}) == 7
    assert sum(len(p["packages"]) for p in projects) == 9
    assert topology["shared_database"] is False and manifest["capital_authorized"] is False
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
    print("seven repositories, nine distributions and immutable remote sources verified")


if __name__ == "__main__":
    main()
