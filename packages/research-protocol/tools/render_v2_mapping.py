"""Render the V2 <-> contract mapping tables of SPEC_V2.md from the packaged domain registry.

The block between the MAPPING markers of SPEC_V2.md is generated; tests/v2/test_v2_spec.py fails
if it drifts from domains.json. Usage: python tools/render_v2_mapping.py [--write]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "src" / "research_protocol" / "v2" / "data" / "domains.json"
SPEC = ROOT / "SPEC_V2.md"
BEGIN = "<!-- MAPPING:BEGIN (gerado por tools/render_v2_mapping.py; não editar à mão) -->"
END = "<!-- MAPPING:END -->"

# Where each required domain field lives in the V2 envelope (besides the payload itself).
TASK_HEADER = {
    "request_id": "`request_id` (igual, conferido)",
    "research_id": "`research_id` (igual, conferido)",
    "hypothesis_id": "`hypothesis_id` (igual, conferido)",
    "schema_version": "`payload_schema` (igual, conferido)",
}
RESULT_HEADER = {
    "result_id": "`result.result_id`",
    "experiment_id": "`result.experiment_id`",
    "admission_id": "`result.admission_id`",
    "request_id": "`request_id`",
    "research_id": "`research_id`",
    "hypothesis_id": "`hypothesis_id`",
    "result_state": "`result.result_state`",
    "operational_state": "`result.operational_state`",
    "scientific_state": "`result.scientific_state`",
    "economic_state": "`result.economic_state`",
    "capital_permission": "`result.capital_permission` (sempre `false`)",
    "schema_version": "`result.payload_schema`",
}


def _required(schema: dict) -> list[str]:
    return list(schema.get("required", []))


def render(registry: dict) -> str:
    lines = [BEGIN, ""]
    lines.append(f"Fonte: `predictor-qualification@{registry['source']['commit']}`.")
    lines.append("")
    for name in sorted(registry["domains"]):
        entry = registry["domains"][name]
        lines.append(f"#### `{name}`")
        lines.append("")
        lines.append(f"- Contrato: `{entry['contract']['path']}`, sha256 `{entry['contract']['sha256']}`")
        lines.append(
            f"- `payload_schema` da task: `{entry['request_schema_id']}` (schema copiado sem alteração)"
        )
        lines.append(f"- `payload_schema` do resultado: `{entry['result_schema_id']}`")
        lines.append(f"- `adapter_api`: `{entry['adapter_api']['function']}`")
        lines.append(f"- `adapter_paths`: {', '.join('`' + p + '`' for p in entry['adapter_paths'])}")
        lines.append("")
        lines.append("| Campo obrigatório do pedido | Na `ResearchTaskV2` |")
        lines.append("|---|---|")
        for field in _required(entry["request_schema"]):
            where = TASK_HEADER.get(field, "só no `payload`")
            lines.append(f"| `{field}` | `payload.{field}`; {where} |")
        lines.append(
            "| `client_ref` (opcional no contrato) | `payload.client_ref` = "
            "`{schema: research-client-ref/2, task_id}` (do envelope) |"
        )
        lines.append("")
        lines.append("| Campo do resultado | Na `ResearchResultV2` |")
        lines.append("|---|---|")
        for field in entry["result_required_fields"]:
            where = RESULT_HEADER.get(field, "só no payload")
            lines.append(f"| `{field}` | bytes exatos em `result.payload_canonical`; {where} |")
        lines.append("")
        codes = entry["outcome_exit_codes"]
        lines.append("| Status do outcome | exit | Classe V2 |")
        lines.append("|---|--:|---|")
        classes = {
            "RESULT": "TERMINAL_RESULT",
            "DUPLICATE": "TERMINAL_RESULT",
            "REJECTED": "TERMINAL_REFUSAL",
            "CONFLICT": "TERMINAL_REFUSAL",
            "TEMPORAL_INTEGRITY_VIOLATION": "TERMINAL_REFUSAL",
            "RECONCILIATION_REQUIRED": "REQUIRES_HUMAN",
        }
        for status in sorted(codes, key=lambda s: (codes[s], s)):
            lines.append(f"| `{status}` | {codes[status]} | `{classes.get(status, 'RETRYABLE')}` |")
        lines.append("")
        lines.append(
            "Estados (copiados, nunca traduzidos): "
            f"`result_state` ∈ {{{', '.join(entry['result_states'])}}}; "
            f"`operational_state` ∈ {{{', '.join(entry['operational_states'])}}}; "
            f"`scientific_state` ∈ {{{', '.join(entry['scientific_states'])}}}; "
            f"`economic_state` ∈ {{{', '.join(entry['economic_states'])}}}."
        )
        lines.append("")
    lines.append(END)
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    registry = json.loads(REGISTRY.read_bytes())
    block = render(registry)
    text = SPEC.read_text(encoding="utf-8")
    start, stop = text.index(BEGIN), text.index(END) + len(END)
    updated = text[:start] + block + text[stop:]
    if "--write" in argv:
        SPEC.write_text(updated, encoding="utf-8", newline="\n")
        print("SPEC_V2.md: mapping block written")
        return 0
    if updated != text:
        print("SPEC_V2.md: mapping block is out of date (run with --write)")
        return 1
    print("SPEC_V2.md: mapping block up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
