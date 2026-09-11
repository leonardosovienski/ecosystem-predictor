"""Fail-closed integration check for the three real domain distributions.

Run this only in an environment where cripto-predictor,
brasileirao-predictor and stocks-predictor are installed together.
"""

import json
import os
from importlib.metadata import distribution
from pathlib import Path

from ecosystem.registry import Registry

EXPECTED_DOMAINS = {
    "cripto": "crypto",  # public entry-point name is Portuguese; domain contract is English
    "brasileirao": "brasileirao",
    "stocks": "stocks",
}


def main() -> int:
    manifest = json.loads(Path("registries/compatibility_candidate.json").read_text())
    for name, expected in manifest["consumers"].items():
        if name == "cain":
            continue
        installed = distribution(name)
        direct = json.loads(installed.read_text("direct_url.json") or "{}")
        if (
            installed.version != expected["version"]
            or direct.get("vcs_info", {}).get("commit_id") != expected["commit"]
        ):
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
            json.dumps({"status": "PASS", "manifest": manifest, "diagnostics": diagnostics}, indent=2),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
