"""Fixed allowlist of domain adapters, loaded by module name (SPEC V2 §9).

The domains get no console script and no dependency on this package: the consumer imports the adapter that
lives in the domain's ``adapter_paths``. Nothing from a task, a file or the command line chooses the module;
a domain without an entry here has no consumer. The other two domains add their entry in their own Stage B
mission.

Adapter interface (duck-typed, checked at load time):
    identity() -> {"distribution", "version", "module"}
    submit_task(task: dict, config: dict) -> outcome   # through the domain's adapter_api, request_bytes(task)
    reread(request_id: str, config: dict) -> (exit_code, payload)   # the domain's authoritative re-read
"""

from __future__ import annotations

import importlib
from types import MappingProxyType, ModuleType

ADAPTERS = MappingProxyType(
    {
        "crypto": MappingProxyType(
            {"distribution": "cripto-predictor", "module": "GarimpoInvestimentos.adapters.research_v2"}
        ),
        "stocks": MappingProxyType(
            {"distribution": "stocks-predictor", "module": "stocks_predictor.adapters.research_v2"}
        ),
        "brasileirao": MappingProxyType(
            {"distribution": "brasileirao-predictor", "module": "brasileirao_predictor.adapters.research_v2"}
        ),
    }
)
REQUIRED = ("identity", "submit_task", "reread")


class AdapterUnavailable(RuntimeError):
    code = "ADAPTER_UNAVAILABLE"


def load(domain: str) -> ModuleType:
    entry = ADAPTERS.get(domain)
    if entry is None:
        raise AdapterUnavailable(f"no adapter registered for domain {domain[:40]!r}")
    try:
        module = importlib.import_module(entry["module"])
    except ImportError as exc:
        raise AdapterUnavailable(f"{entry['module']} not importable: {exc}") from exc
    missing = [name for name in REQUIRED if not callable(getattr(module, name, None))]
    if missing or getattr(module, "DOMAIN", None) != domain:
        raise AdapterUnavailable(f"{entry['module']} does not implement the adapter interface for {domain}")
    identity = module.identity()
    if identity.get("distribution") != entry["distribution"] or identity.get("module") != entry["module"]:
        raise AdapterUnavailable(f"{entry['module']} reports another identity: {identity}")
    return module
