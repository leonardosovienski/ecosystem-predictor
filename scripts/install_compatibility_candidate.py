"""Install only the declared immutable candidates into an explicit test environment."""

import argparse
import json
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", required=True)
    parser.add_argument("--manifest", type=Path, default=Path("registries/compatibility_candidate.json"))
    args = parser.parse_args()
    record = json.loads(args.manifest.read_text())
    requirements = [
        value["url"] + "#" + value["hash"].replace(":", "=", 1) for value in record["shared"].values()
    ]
    subprocess.run([args.python, "-m", "pip", "install", *requirements], check=True)
    domains = [
        "git+" + value["repository"] + ".git@" + value["commit"]
        for name, value in record["consumers"].items()
        if name != "cain"
    ]
    subprocess.run([args.python, "-m", "pip", "install", ".", *domains], check=True)


if __name__ == "__main__":
    main()
