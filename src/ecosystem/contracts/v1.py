"""Contract v1: the canonical plugin protocol and wire shapes.

This is the FIRST version of a contract that, as of this session, no
existing domain plugin (f1/cs/lol/cripto/brasileirao) fully implements —
see docs/adr/0001-plugin-protocol-v1.md for the concrete gaps found in each
repository and what each one needs to change to comply. The registry
(``ecosystem.registry``) is defensive about non-compliant plugins: it loads
what it can and reports the rest as degraded capabilities rather than
crashing the aggregator, but a plugin that doesn't implement at least
``health()`` is rejected outright (fail-closed).
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, Field


class OperationalStatus(StrEnum):
    """Union of the canonical status values actually observed across the
    ecosystem's domain plugins this cycle (lol/cs/cripto health() payloads).
    A domain reporting a status outside this set is a contract violation,
    not a new legitimate state — extend this enum deliberately, don't widen
    silently in a plugin adapter."""

    SUCCEEDED = "SUCCEEDED"
    DEGRADED = "DEGRADED"
    WAITING = "WAITING"
    FAILED = "FAILED"
    SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"
    NO_UPSTREAM_EVENTS = "NO_UPSTREAM_EVENTS"
    CLOSED_BY_HUMAN_DECISION = "CLOSED_BY_HUMAN_DECISION"


class HealthReport(BaseModel):
    """Typed replacement for the ad-hoc dicts each plugin returns today."""

    domain: str
    status: OperationalStatus
    version: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class CapabilityManifest(BaseModel):
    """What a domain plugin can actually do, declared up front so the
    gateway can fail closed on a route the domain never claimed to support,
    instead of discovering it via a runtime AttributeError."""

    domain: str
    supports_prediction: bool = False
    supports_settlement: bool = False
    supports_collection: bool = False
    scientific_status: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class PredictionRequest(BaseModel):
    """Envelope around a domain-specific payload. The aggregator does not
    know or validate the shape of ``payload`` — that is the domain's own
    contract (e.g. lol-predictor's PredictionRequest). This envelope only
    carries what the aggregator needs to route, authorize, and trace the
    call without importing anything from the target domain's checkout."""

    domain: str
    run_id: str
    payload: dict[str, Any] = Field(default_factory=dict)


class PredictionResponse(BaseModel):
    domain: str
    run_id: str
    status: OperationalStatus
    payload: dict[str, Any] = Field(default_factory=dict)


@runtime_checkable
class PluginV1(Protocol):
    """Structural contract a domain plugin should satisfy to be served
    in-process by the gateway. ``predict`` is intentionally not part of
    this Protocol's required surface: cripto-predictor is research-only
    today (no predict() at all) and that is a legitimate, documented
    state (BLOCKED_PENDING_SECRET_ROTATION), not a bug. The registry
    checks for ``predict`` with ``hasattr`` at dispatch time and returns
    503 (fail-closed) rather than assuming every plugin implements it."""

    domain: str

    def health(self) -> HealthReport: ...

    def capabilities(self) -> CapabilityManifest: ...
