"""Plugin discovery and the registry the gateway dispatches through.

Canonical entry-point group: ``predictor.plugins``. The current Cripto,
Brasileirão and Stocks distributions all publish their adapters through this
group. Their adapter modules must live in domain-specific top-level packages;
generic packages such as ``src`` or ``scripts`` are forbidden because Python
can otherwise resolve one domain's adapter from another installed wheel.

The cross-repository integration check in
``scripts/check_real_plugin_integration.py`` is the executable source of truth:
it discovers all three real distributions in one environment and verifies
identity, domain and health isolation pairwise.
"""

from __future__ import annotations

import logging
from collections import Counter
from dataclasses import dataclass, field
from importlib.metadata import EntryPoint, entry_points

from ecosystem.contracts import CapabilityManifest, HealthReport, OperationalStatus, PluginV1
from ecosystem.contracts.diagnostics import NativeCapabilities

logger = logging.getLogger("ecosystem.registry")

PLUGIN_GROUP = "predictor.plugins"


@dataclass
class PluginRecord:
    """One discovered entry point and its load outcome. A record with
    ``error`` set means the aggregator knows this domain exists (it was
    declared as an entry point) but could not load it — this is a
    *degraded* capability, reported as such via health/capabilities, never
    silently dropped from the registry."""

    name: str
    entry_point: EntryPoint
    instance: PluginV1 | None = None
    error: str | None = None

    @property
    def loaded(self) -> bool:
        return self.instance is not None


@dataclass
class Registry:
    """In-memory plugin registry, populated once at gateway startup.

    Fail-closed by construction: a domain that is not in ``self.records``,
    or whose record has ``loaded is False``, is treated by the gateway as
    unavailable (503), never silently skipped or defaulted to a stub.
    """

    records: dict[str, PluginRecord] = field(default_factory=dict)

    @classmethod
    def discover(cls, *, group: str = PLUGIN_GROUP) -> Registry:
        registry = cls()
        discovered = sorted(
            entry_points(group=group),
            key=lambda ep: (
                ep.name,
                ep.value,
                ep.dist.metadata["Name"] if ep.dist else "",
                ep.dist.version if ep.dist else "",
            ),
        )
        counts = Counter(ep.name for ep in discovered)
        for ep in discovered:
            if counts[ep.name] > 1:
                registry.records[ep.name] = PluginRecord(
                    name=ep.name, entry_point=ep, error="duplicate entry-point name"
                )
            else:
                registry._load_one(ep)
        return registry

    def diagnostic_snapshot(self) -> dict[str, dict]:
        """V2 diagnostics retain literal producer payloads, without status translation.

        INVALID describes the contract, not the producer's scientific state.
        This optional registry never grants permission to execute capital.
        """
        result: dict[str, dict] = {}
        for name, record in self.records.items():
            distribution = record.entry_point.dist
            diagnostic: dict = {
                "schema_version": "plugin-diagnostics/2",
                "origin": {
                    "entry_point": record.entry_point.value,
                    "distribution": distribution.metadata["Name"] if distribution else None,
                    "version": distribution.version if distribution else None,
                },
                "capital_authorized_by_diagnostic": False,
            }
            for method, model in (("health", HealthReport), ("capabilities", NativeCapabilities)):
                payload = None
                try:
                    if record.instance is None:
                        raise ValueError(record.error or "plugin unavailable")
                    raw = getattr(record.instance, method)()
                    payload = raw.model_dump(mode="json") if hasattr(raw, "model_dump") else raw
                    model.model_validate(payload)
                except Exception as exc:  # noqa: BLE001
                    diagnostic[method] = {
                        "contract_status": "INVALID",
                        "payload": payload,
                        "error_type": type(exc).__name__,
                    }
                else:
                    legacy = HealthReport if method == "health" else CapabilityManifest
                    try:
                        legacy.model_validate(payload)
                    except Exception:  # noqa: BLE001
                        legacy_status = "INVALID"
                    else:
                        legacy_status = "VALID"
                    diagnostic[method] = {
                        "contract_status": "VALID",
                        "payload": payload,
                        "state_namespace": payload["domain"],
                        "legacy_v1_contract_status": legacy_status,
                        "state_mapping": None,
                    }
            result[name] = diagnostic
        return result

    def _load_one(self, ep: EntryPoint) -> None:
        try:
            target = ep.load()
            instance = target() if isinstance(target, type) else target
        except Exception as exc:  # noqa: BLE001 - a broken plugin must not take down the gateway
            logger.error("plugin %r failed to load: %s", ep.name, exc)
            self.records[ep.name] = PluginRecord(name=ep.name, entry_point=ep, error=str(exc))
            return

        # callable(), not hasattr(): a plugin could still declare
        # `capabilities` as a non-callable class attribute (a tuple, say)
        # instead of a method. hasattr() alone would call that compliant
        # here and only fail later when the gateway actually tries
        # `.capabilities()`. lol-predictor's plugin.py used to do exactly
        # this; it was fixed upstream and verified compliant on
        # 2026-08-03 - see docs/adr/0001-plugin-protocol-v1.md.
        health_callable = callable(getattr(instance, "health", None))
        capabilities_callable = callable(getattr(instance, "capabilities", None))
        if not (health_callable and capabilities_callable):
            message = (
                f"plugin {ep.name!r} does not implement PluginV1 "
                "(health()/capabilities() must be callable methods) - registered as degraded"
            )
            logger.warning(message)
            self.records[ep.name] = PluginRecord(name=ep.name, entry_point=ep, error=message)
            return

        self.records[ep.name] = PluginRecord(name=ep.name, entry_point=ep, instance=instance)

    def get(self, name: str) -> PluginRecord | None:
        return self.records.get(name)

    def list_domains(self) -> list[str]:
        return sorted(self.records)

    def health_snapshot(self) -> dict[str, HealthReport]:
        """Best-effort health for every registered domain. A domain whose
        plugin failed to load reports FAILED without ever calling into it -
        there's nothing to call."""
        snapshot: dict[str, HealthReport] = {}
        for name, record in self.records.items():
            if not record.loaded:
                snapshot[name] = HealthReport(
                    domain=name, status=OperationalStatus.FAILED, details={"error": record.error}
                )
                continue
            try:
                raw = record.instance.health()  # type: ignore[union-attr]
                payload = raw.model_dump(mode="python") if hasattr(raw, "model_dump") else raw
                snapshot[name] = HealthReport.model_validate(payload)
            except Exception as exc:  # noqa: BLE001
                snapshot[name] = HealthReport(
                    domain=name, status=OperationalStatus.FAILED, details={"error": str(exc)}
                )
        return snapshot

    def capability_snapshot(self) -> dict[str, CapabilityManifest]:
        snapshot: dict[str, CapabilityManifest] = {}
        for name, record in self.records.items():
            if not record.loaded:
                snapshot[name] = CapabilityManifest(domain=name, extra={"error": record.error})
                continue
            try:
                raw = record.instance.capabilities()  # type: ignore[union-attr]
                payload = raw.model_dump(mode="python") if hasattr(raw, "model_dump") else raw
                snapshot[name] = CapabilityManifest.model_validate(payload)
            except Exception as exc:  # noqa: BLE001
                snapshot[name] = CapabilityManifest(domain=name, extra={"error": str(exc)})
        return snapshot
