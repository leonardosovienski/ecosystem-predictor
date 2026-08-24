"""Contract v1: canonical plugin protocol and cross-domain state vocabulary.

The current economic domains are crypto, brasileirao and stocks. The registry
loads them through the ``predictor.plugins`` entry-point group. Operational,
scientific, predictive and economic state are intentionally separate: a green
job is not scientific evidence, predictive skill is not economic edge, and no
state authorizes capital by implication.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, Field


class OperationalStatus(StrEnum):
    SUCCEEDED = "SUCCEEDED"
    DEGRADED = "DEGRADED"
    WAITING = "WAITING"
    FAILED = "FAILED"
    SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"
    NO_UPSTREAM_EVENTS = "NO_UPSTREAM_EVENTS"
    CLOSED_BY_HUMAN_DECISION = "CLOSED_BY_HUMAN_DECISION"


class ScientificStatus(StrEnum):
    UNKNOWN = "UNKNOWN"
    RESEARCH_ONLY = "RESEARCH_ONLY"
    M0 = "M0"
    ACTIVE_HYPOTHESIS = "ACTIVE_HYPOTHESIS"
    INCONCLUSIVE = "INCONCLUSIVE"
    SIGNAL_DEMONSTRATED = "SIGNAL_DEMONSTRATED"
    NO_GO = "NO_GO"
    CLOSED_NO_GO = "CLOSED_NO_GO"


class PredictiveStatus(StrEnum):
    UNKNOWN = "UNKNOWN"
    NOT_TESTED_REAL_DATA = "NOT_TESTED_REAL_DATA"
    NOT_DEMONSTRATED = "NOT_DEMONSTRATED"
    INCONCLUSIVE = "INCONCLUSIVE"
    BEATS_BASELINE = "BEATS_BASELINE"
    PROSPECTIVE_VALIDATION = "PROSPECTIVE_VALIDATION"
    PROSPECTIVELY_VALIDATED = "PROSPECTIVELY_VALIDATED"


class EconomicStatus(StrEnum):
    UNKNOWN = "UNKNOWN"
    NOT_DEFINED = "NOT_DEFINED"
    NOT_TESTED = "NOT_TESTED"
    NOT_VALIDATED = "NOT_VALIDATED"
    HISTORICAL_NO_GO = "HISTORICAL_NO_GO"
    SHADOW_VALIDATION = "SHADOW_VALIDATION"
    ECONOMICALLY_VALIDATED = "ECONOMICALLY_VALIDATED"


class CapitalPermission(StrEnum):
    FORBIDDEN = "FORBIDDEN"
    MANUAL_ONLY = "MANUAL_ONLY"
    AUTHORIZED = "AUTHORIZED"


class HealthReport(BaseModel):
    """Operational health only; never a scientific/economic verdict."""

    domain: str
    status: OperationalStatus
    version: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class CapabilityManifest(BaseModel):
    """Domain capabilities plus orthogonal governance states.

    Fields default to UNKNOWN/forbidden so a partially migrated plugin fails
    closed rather than being promoted by absence of information.
    """

    domain: str
    supports_prediction: bool = False
    supports_settlement: bool = False
    supports_collection: bool = False
    supports_no_opportunity: bool = True
    scientific_status: ScientificStatus = ScientificStatus.UNKNOWN
    predictive_status: PredictiveStatus = PredictiveStatus.UNKNOWN
    economic_status: EconomicStatus = EconomicStatus.UNKNOWN
    capital_permission: CapitalPermission = CapitalPermission.FORBIDDEN
    extra: dict[str, Any] = Field(default_factory=dict)


class PredictionRequest(BaseModel):
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
    """Minimum in-process integration surface for a canonical predictor."""

    domain: str

    def health(self) -> HealthReport: ...

    def capabilities(self) -> CapabilityManifest: ...
