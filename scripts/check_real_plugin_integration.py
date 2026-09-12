"""Fail-closed integration check for the three real domain distributions.

Run this only in an environment where cripto-predictor,
brasileirao-predictor and stocks-predictor are installed together.
"""

import argparse
import hashlib
import json
import os
import re
from importlib.metadata import distribution
from pathlib import Path

from ecosystem.registry import Registry

EXPECTED_DOMAINS = {
    "cripto": "crypto",  # public entry-point name is Portuguese; domain contract is English
    "brasileirao": "brasileirao",
    "stocks": "stocks",
}


def candidate_matches(installed, expected: dict) -> bool:
    """Require the declared version and immutable VCS or wheel provenance."""
    direct = json.loads(installed.read_text("direct_url.json") or "{}")
    if installed.version != expected["version"]:
        return False
    if "wheel_sha256" in expected:
        digest = expected["wheel_sha256"]
        return (
            isinstance(digest, str)
            and re.fullmatch(r"[a-f0-9]{64}", digest) is not None
            and direct.get("archive_info", {}).get("hashes", {}).get("sha256") == digest
        )
    commit = expected.get("commit")
    return (
        isinstance(commit, str)
        and re.fullmatch(r"[a-f0-9]{40}", commit) is not None
        and direct.get("vcs_info", {}).get("commit_id") == commit
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args(argv)
    released_mode = os.environ.get("RELEASED_WHEELS") == "1"
    if released_mode and args.manifest is not None:
        parser.error("A candidate manifest cannot certify released wheels")
    manifest_path = args.manifest or Path("registries/compatibility_candidate.json")
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    if released_mode:
        released = json.loads(Path("registries/released_architecture.json").read_text())
        names = {
            "predictor-core",
            "predictor-ops",
            "ecosystem-predictor",
            "cripto-predictor",
            "stocks-predictor",
            "brasileirao-predictor",
        }
        for wheel in (
            wheel for repo in released["repositories"] for wheel in repo["wheels"] if wheel["name"] in names
        ):
            installed = distribution(wheel["name"])
            direct = json.loads(installed.read_text("direct_url.json") or "{}")
            if (
                installed.version != wheel["version"]
                or direct.get("archive_info", {}).get("hashes", {}).get("sha256") != wheel["sha256"]
            ):
                raise SystemExit(f"published wheel mismatch: {wheel['name']}")
    for name, expected in manifest["consumers"].items():
        if name == "cain" or released_mode:
            continue
        installed = distribution(name)
        if not candidate_matches(installed, expected):
            raise SystemExit(f"candidate distribution mismatch: {name}")
    for name, expected in manifest["shared"].items():
        installed = distribution(name)
        direct = json.loads(installed.read_text("direct_url.json") or "{}")
        hashes = direct.get("archive_info", {}).get("hashes", {})
        if (
            installed.version != expected["version"]
            or "sha256:" + hashes.get("sha256", "") != expected["hash"]
        ):
            raise SystemExit(f"shared wheel mismatch: {name}")
    registry = Registry.discover()
    missing = set(EXPECTED_DOMAINS).difference(registry.records)
    if missing:
        raise SystemExit(f"missing real plugins: {sorted(missing)}")

    records = {name: registry.get(name) for name in EXPECTED_DOMAINS}
    for name, record in records.items():
        if record is None or not record.loaded:
            error = None if record is None else record.error
            raise SystemExit(f"plugin {name!r} failed to load: {error}")

    instances = [records[name].instance for name in sorted(EXPECTED_DOMAINS)]
    if len({id(instance) for instance in instances}) != len(instances):
        raise SystemExit("plugin identity collision: two domains loaded the same object")

    diagnostics = registry.diagnostic_snapshot()
    for name, expected_domain in EXPECTED_DOMAINS.items():
        for method in ("health", "capabilities"):
            if diagnostics[name][method]["contract_status"] != "VALID":
                raise SystemExit(f"invalid {method} contract for {name!r}")
            report = diagnostics[name][method]
            if report["payload"]["domain"] != expected_domain:
                raise SystemExit(f"{method} domain mismatch for {name!r}")
            if report["state_namespace"] != expected_domain or report["state_mapping"] is not None:
                raise SystemExit(f"implicit state translation for {name!r}")
        capabilities = diagnostics[name]["capabilities"]["payload"]
        if "error" in capabilities["extra"]:
            raise SystemExit(f"fallback response for {name!r}")
        if capabilities["capital_permission"] != "FORBIDDEN":
            raise SystemExit(f"unexpected capital declaration for {name!r}")
    stocks = diagnostics["stocks"]["capabilities"]["payload"]
    assert [stocks[key] for key in ("scientific_status", "predictive_status", "economic_status")] == [
        "DISCOVERY_INCONCLUSIVE",
        "NO_VALIDATED_NET_EDGE",
        "NO_GO",
    ]

    print("real plugin integration OK: cripto, brasileirao and stocks are isolated")
    if destination := os.environ.get("COMPATIBILITY_RECEIPT"):
        Path(destination).write_text(
            json.dumps(
                {
                    "status": "PASS",
                    "manifest": manifest,
                    "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
                    "released_wheels": released_mode,
                    "diagnostics": diagnostics,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
