"""Renovação agendada dos atestados de harness do cripto em `registries/harness_registry.json`.

Os atestados `pipeline-power/2` do cripto valem 7 dias. Vencidos e ainda `ALIGNED`, deixam o
`check_offline` (e o job `quality` do CI) vermelho — foi o IC-F004 da integration-crypto em 2026-09-27.
O workflow `.github/workflows/crypto-harness-renewal.yml` chama este script:

  decide  escreve em `GITHUB_OUTPUT` `renew=true|false` (não há, para cada métrica, atestado `ALIGNED`
          do cripto válido por mais `renew_when_valid_for_less_than_hours`) e `expired=true|false`
          (há `ALIGNED` já vencido);
  apply   registra os atestados novos (copiados byte a byte para `docs/engineering_controls/<AAAAMMDD>/`)
          como `ALIGNED`, marca os `ALIGNED` anteriores da mesma métrica como `SUPERSEDED` (ainda válidos,
          substituídos por reemissão genuína) e os já vencidos como `EXPIRED` com `reissue_required`
          (precedente de 09d2844), e atualiza `last_verified_at`.

O commit do cripto que o harness certifica, o sha do Core e o limiar ficam em
`registries/harness_renewal.json` e só mudam por PR. O script nunca inventa um atestado: só registra os
arquivos que o harness oficial gravou, e recusa os que não batem com o commit, o Core ou a métrica.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "cripto-predictor"
FILES = {
    "psr": "crypto-trials.harness_attestation.json",
    "spearman_ic": "crypto-trials.phase1_harness_attestation.json",
}
SOURCES = {"psr": "trials.harness_attestation.json", "spearman_ic": "trials.phase1_harness_attestation.json"}
SCOPE = "Synthetic judge power controls only; no economic verdict, trading action or capital authorization"
EXPIRED_BASIS = (
    "Official installed Crypto harness with fixed edge/noise seeds and canonical Core; expired at the "
    "recorded boundary and requires genuine reissue; original evidence unchanged"
)


def _time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _load(root: Path, name: str) -> dict:
    return json.loads((root / "registries" / name).read_text(encoding="utf-8"))


def _aligned(registry: dict) -> list[dict]:
    return [item for item in registry["harnesses"] if item["repo"] == REPO and item["status"] == "ALIGNED"]


def decide(registry: dict, config: dict, now: datetime) -> dict:
    horizon = now + timedelta(hours=config["renew_when_valid_for_less_than_hours"])
    renew = False
    for metric in FILES:
        valid = [_time(item["expires_at"]) for item in _aligned(registry) if item.get("metric") == metric]
        if not valid or max(valid) <= horizon:
            renew = True
    expired = [item["evidence_path"] for item in _aligned(registry) if _time(item["expires_at"]) <= now]
    return {"renew": renew, "expired": bool(expired), "expired_evidence": expired}


def _new_entry(att: dict, metric: str, raw: bytes, evidence_path: str, config: dict) -> dict:
    return {
        "repo": REPO,
        "harness_version": att["schema_version"],
        "reported_core_version": att["core_version"],
        "core_code_sha": config["core_code_sha"],
        "domain_code_version": att["code_version"],
        "executed_at": att["passed_at"],
        "expires_at": att["expires_at"],
        "status": "ALIGNED",
        "reissue_required": False,
        "metric": metric,
        "pipeline_fingerprint": att["pipeline_fingerprint"],
        "evidence_path": evidence_path,
        "evidence_sha256": hashlib.sha256(raw).hexdigest(),
        "scope": SCOPE,
        "basis": (
            "Scheduled genuine clean-tree reissue (crypto-harness-renewal) against Core "
            f"{att['core_version']} on {config['source']['github']}@{config['source']['commit'][:12]}; "
            "attestations staged outside the domain repository; fixed edge/noise controls passed"
        ),
    }


def apply(root: Path, registry: dict, config: dict, now: datetime, attestations: Path | None) -> dict:
    changed: dict[str, list[str]] = {"expired": [], "superseded": [], "added": []}
    for item in _aligned(registry):
        if _time(item["expires_at"]) <= now:
            item.update(status="EXPIRED", reissue_required=True, basis=EXPIRED_BASIS)
            changed["expired"].append(item["evidence_path"])
    if attestations is not None:
        day = now.strftime("%Y%m%d")
        target = root / "docs" / "engineering_controls" / day
        commit = config["source"]["commit"]
        for metric in FILES:
            raw = (attestations / SOURCES[metric]).read_bytes()
            att = json.loads(raw)
            problems = [
                name
                for name, ok in (
                    ("schema_version", att.get("schema_version") == "pipeline-power/2"),
                    ("metric", att.get("metric") == metric),
                    ("core_version", att.get("core_version") == registry["current_released_core_version"]),
                    ("code_version", str(att.get("code_version", "")).endswith(f";git:{commit}")),
                    ("expires_at", _time(att["expires_at"]) > now),
                )
                if not ok
            ]
            if problems:
                raise SystemExit(f"atestado {metric} recusado: {problems}")
            evidence = target / FILES[metric]
            if evidence.exists() and evidence.read_bytes() != raw:
                raise SystemExit(f"{evidence} já existe com outro conteúdo")
            target.mkdir(parents=True, exist_ok=True)
            evidence.write_bytes(raw)
            relative = evidence.relative_to(root).as_posix()
            if any(item.get("evidence_path") == relative for item in registry["harnesses"]):
                continue
            for item in _aligned(registry):
                if item.get("metric") == metric:
                    item.update(
                        status="SUPERSEDED",
                        reissue_required=False,
                        basis=(
                            f"Superseded by the genuine reissue of {att['passed_at']} ({relative}); this "
                            f"attestation stays valid until {item['expires_at']}; original evidence unchanged"
                        ),
                    )
                    changed["superseded"].append(item["evidence_path"])
            registry["harnesses"].append(_new_entry(att, metric, raw, relative, config))
            changed["added"].append(relative)
    if any(changed.values()):
        registry["last_verified_at"] = now.date().isoformat()
    return changed


def _output(values: dict) -> None:
    target = os.environ.get("GITHUB_OUTPUT")
    if target:
        with open(target, "a", encoding="utf-8") as handle:
            for key, value in values.items():
                if isinstance(value, bool):
                    handle.write(f"{key}={'true' if value else 'false'}\n")
    print(json.dumps(values, ensure_ascii=False))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=("decide", "apply"))
    parser.add_argument(
        "--attestations", type=Path, help="pasta com os atestados que o harness oficial gravou"
    )
    parser.add_argument("--now", help="instante UTC ISO-8601 (testes); padrão: agora")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    now = _time(args.now) if args.now else datetime.now(UTC)
    registry, config = _load(args.root, "harness_registry.json"), _load(args.root, "harness_renewal.json")
    if args.command == "decide":
        _output(decide(registry, config, now))
        return 0
    changed = apply(args.root, registry, config, now, args.attestations)
    path = args.root / "registries" / "harness_registry.json"
    path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _output({"changed": any(changed.values())} | changed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
