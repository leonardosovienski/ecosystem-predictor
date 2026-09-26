"""Build src/research_protocol/v2/data/domains.json from the three DOMAIN_RESEARCH_CONTRACT.json.

The request schemas, result fields and state enums are copied verbatim from the contracts in a
predictor-qualification checkout at a given commit (the contract sha256 is recorded). The
outcome statuses and their exit codes are not a separate contract field; they come from the
``EXIT_CODES`` table each domain declares in its contract module (cited below) and can be
checked against the installed domain wheels with ``--verify-installed``.

Usage:
  python tools/build_v2_domain_registry.py --qualification DIR --commit SHA [--check] [--verify-installed]
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "src" / "research_protocol" / "v2" / "data" / "domains.json"
DOMAINS = ("crypto", "brasileirao", "stocks")
# Contract module that declares OUTCOME_STATUSES / EXIT_CODES in each domain (adapter_api path).
CONTRACT_MODULES = {
    "crypto": "GarimpoInvestimentos.research_contract",
    "brasileirao": "brasileirao_predictor.research_runtime.contract",
    "stocks": "stocks_predictor.research_contract",
}
_BASE_EXIT_CODES = {
    "RESULT": 0,
    "DUPLICATE": 0,
    "REJECTED": 2,
    "CONFLICT": 2,
    "NOT_READY": 3,
    "OPS_FAILED_RETRYABLE": 3,
    "TEMPORAL_INTEGRITY_VIOLATION": 4,
    "RECONCILIATION_REQUIRED": 5,
}
OUTCOME_EXIT_CODES = {
    # GarimpoInvestimentos/research_contract.py EXIT_CODES (cripto-predictor 1.2.0rc2)
    "crypto": dict(_BASE_EXIT_CODES),
    # brasileirao_predictor/research_runtime/contract.py EXIT_CODES (brasileirao-predictor 0.3.0rc3)
    "brasileirao": dict(_BASE_EXIT_CODES),
    # stocks_predictor/research_contract.py EXIT_CODES (stocks-predictor 0.3.0rc2)
    "stocks": dict(_BASE_EXIT_CODES, STATE_BUSY_RETRYABLE=3, STORAGE_FAILED_RETRYABLE=3),
}


def _git_show(repo: Path, commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"], check=True, capture_output=True
    ).stdout


def build(repo: Path, commit: str) -> dict:
    full = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", f"{commit}^{{commit}}"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    domains = {}
    for name in DOMAINS:
        path = f"qualification/{name}/DOMAIN_RESEARCH_CONTRACT.json"
        raw = _git_show(repo, full, path)
        contract = json.loads(raw)
        if contract["domain_prefix"] != name:
            raise SystemExit(f"{path}: domain_prefix {contract['domain_prefix']!r} != {name!r}")
        request_schema = contract["request_schema"]
        result_schema = contract["result_schema"]
        distinct = result_schema["distinct_states"]
        domains[name] = {
            "contract": {"path": path, "sha256": hashlib.sha256(raw).hexdigest()},
            "request_schema_id": request_schema["$id"],
            "request_schema": request_schema,
            "result_schema_id": result_schema["id"],
            "result_required_fields": sorted(result_schema["top_level"]),
            "result_states": list(contract["result_states"]),
            "operational_states": list(distinct["operational_state"]),
            "scientific_states": list(distinct["scientific_state"]),
            "economic_states": list(distinct["economic_state"]),
            "outcome_exit_codes": OUTCOME_EXIT_CODES[name],
            "adapter_paths": list(contract["adapter_paths"]),
            "adapter_api": contract["adapter_api"],
        }
    return {
        "schema": "research-protocol-v2-domains/1",
        "source": {
            "repository": "leonardosovienski/predictor-qualification",
            "commit": full,
        },
        "domains": domains,
    }


def render(registry: dict) -> bytes:
    return (json.dumps(registry, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def verify_installed(registry: dict) -> list[str]:
    problems = []
    for name, entry in registry["domains"].items():
        module = importlib.import_module(CONTRACT_MODULES[name])
        checks = {
            "request_schema_id": module.REQUEST_SCHEMA,
            "result_schema_id": module.RESULT_SCHEMA,
            "outcome_exit_codes": dict(module.EXIT_CODES),
            "result_states": list(module.RESULT_STATES),
            "operational_states": list(module.OPERATIONAL_STATES),
            "scientific_states": list(module.SCIENTIFIC_STATES),
            "economic_states": list(module.ECONOMIC_STATES),
        }
        for key, installed in checks.items():
            if entry[key] != installed:
                problems.append(f"{name}.{key}: registry {entry[key]!r} != installed {installed!r}")
        if set(entry["outcome_exit_codes"]) != set(module.OUTCOME_STATUSES):
            problems.append(f"{name}: outcome statuses differ from installed OUTCOME_STATUSES")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qualification", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--check", action="store_true", help="fail if domains.json differs")
    parser.add_argument("--verify-installed", action="store_true")
    args = parser.parse_args(argv)
    registry = build(args.qualification, args.commit)
    data = render(registry)
    if args.verify_installed:
        problems = verify_installed(registry)
        for line in problems:
            print("INSTALLED MISMATCH:", line)
        if problems:
            return 1
        print("installed domain contract modules: OK")
    if args.check:
        current = OUT.read_bytes() if OUT.exists() else b""
        if current != data:
            print(f"{OUT} is out of date")
            return 1
        print(f"{OUT.name}: up to date (sha256 {hashlib.sha256(data).hexdigest()})")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(data)
    print(f"wrote {OUT} (sha256 {hashlib.sha256(data).hexdigest()})")
    for name, entry in registry["domains"].items():
        print(f"  {name}: contract {entry['contract']['sha256']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
