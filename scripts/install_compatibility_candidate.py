"""Install only the declared immutable candidates into an explicit test environment."""

import argparse
import json
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", required=True)
    parser.add_argument("--manifest", type=Path, default=Path("registries/compatibility_candidate.json"))
    parser.add_argument(
        "--released", action="store_true", help="Install published wheels instead of VCS candidates"
    )
    args = parser.parse_args()
    if args.released:
        released = json.loads(Path("registries/released_architecture.json").read_text())
        names = {
            "predictor-core",
            "predictor-ops",
            "ecosystem-predictor",
            "cripto-predictor",
            "stocks-predictor",
            "brasileirao-predictor",
        }
        wheels = [
            wheel for repo in released["repositories"] for wheel in repo["wheels"] if wheel["name"] in names
        ]
        assert {wheel["name"] for wheel in wheels} == names and len(wheels) == len(names)
        subprocess.run(
            [
                args.python,
                "-m",
                "pip",
                "install",
                *[wheel["url"] + "#sha256=" + wheel["sha256"] for wheel in wheels],
            ],
            check=True,
        )
        return
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
