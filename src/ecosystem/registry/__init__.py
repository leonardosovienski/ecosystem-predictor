"""Plugin discovery and the registry the gateway dispatches through.

Canonical entry-point group: ``predictor.plugins``. This is a deliberate
choice, not a discovery of existing consensus — as of this session,
lol-predictor and cs-predictor already use this group name, but
cripto-predictor uses ``ecosystem_predictor.plugins`` instead, and
f1-predictor/brasileirao-predictor declare no plugin entry point at all.
See docs/adr/0001-plugin-protocol-v1.md for the full inventory and the
required follow-up in each domain repository (out of scope for this
session, which works only on the aggregator).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from importlib.metadata import EntryPoint, entry_points

from ecosystem.contracts import CapabilityManifest, HealthReport, OperationalStatus, PluginV1

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
        for ep in entry_points(group=group):
            registry._load_one(ep)
        return registry

    def _load_one(self, ep: EntryPoint) -> None:
        try:
            target = ep.load()
            instance = target() if isinstance(target, type) else target
        except Exception as exc:  # noqa: BLE001 - a broken plugin must not take down the gateway
            logger.error("plugin %r failed to load: %s", ep.name, exc)
            self.records[ep.name] = PluginRecord(name=ep.name, entry_point=ep, error=str(exc))
            return

        # callable(), not hasattr(): lol-predictor's real plugin.py today
        # declares `capabilities` as a class *attribute* (a tuple), not a
        # method. hasattr() alone would call that compliant here and only
        # fail later when the gateway actually tries `.capabilities()` -
        # see docs/adr/0001-plugin-protocol-v1.md.
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
