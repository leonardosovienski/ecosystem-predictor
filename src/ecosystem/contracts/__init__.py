"""Versioned wire and plugin contracts for the ecosystem aggregator.

Contracts are versioned by module (``v1``, ``v2``, ...), never mutated in
place. A breaking change to a shape always lands in a new module; the
gateway can serve multiple versions side by side during a migration.
"""

from ecosystem.contracts.v1 import (
    CapabilityManifest,
    HealthReport,
    OperationalStatus,
    PluginV1,
    PredictionRequest,
    PredictionResponse,
)

__all__ = [
    "CapabilityManifest",
    "HealthReport",
    "OperationalStatus",
    "PluginV1",
    "PredictionRequest",
    "PredictionResponse",
]
