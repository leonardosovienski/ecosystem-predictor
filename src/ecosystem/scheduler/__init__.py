"""Ecosystem-level scheduled jobs, run through predictor_ops's job runner
(lock/heartbeat/timeout/redaction) exactly like every domain's own
scheduler - the aggregator does not reinvent process supervision."""

from __future__ import annotations

import sys
from pathlib import Path

from predictor_ops import JobConfig, run_job
from predictor_ops.models import RuntimeConfig


def probe_domains_job(*, runtime_root: Path, timeout_seconds: float = 30.0) -> JobConfig:
    """A JobConfig that re-invokes this same package's health-probe CLI as
    a subprocess - the same shape every domain uses for its own scheduled
    work, so predictor_ops's lock/heartbeat/timeout semantics apply
    identically here."""
    return JobConfig(
        id="ecosystem-probe-domains",
        command=[sys.executable, "-m", "ecosystem.scheduler.probe"],
        timeout_seconds=timeout_seconds,
        heartbeat_interval_seconds=5.0,
        # This probe has no scientific verdict. Ops transports the value but
        # never infers it from operational success or failure.
        scientific_state=None,
        runtime=RuntimeConfig(root=runtime_root, lock_stale_after_seconds=120),
    )


def run_probe_domains(*, runtime_root: Path) -> int:
    result = run_job(probe_domains_job(runtime_root=runtime_root))
    return result.exit_code
