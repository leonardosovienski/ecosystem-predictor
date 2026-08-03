"""Liveness/readiness. Unauthenticated by design (orchestrators probing
these can't be expected to hold a bearer token) but they leak no domain
data - only aggregate status."""

from __future__ import annotations

from fastapi import APIRouter, Request, Response, status

from ecosystem.contracts import OperationalStatus

router = APIRouter(tags=["health"])


@router.get("/healthz")
def healthz() -> dict:
    """Process is up and can serve HTTP. Does not touch the registry,
    Redis, Postgres, or any domain - that's /readyz's job. A container
    orchestrator should restart the process if this ever fails; it should
    NOT restart on /readyz failing (that's a dependency problem, not a
    process problem)."""
    return {"status": "ok"}


@router.get("/readyz")
def readyz(request: Request, response: Response) -> dict:
    """Fail closed: any required domain missing or degraded means 503,
    never a 200 with a caveat buried in the body. required_domains is
    empty by default (see Settings) until real domain adapters exist -
    an empty required list means readiness never blocks on domain
    availability, which is itself a documented, visible gap (see
    docs/ECOSYSTEM_BLUEPRINT.md), not a silently permissive default."""
    settings = request.app.state.settings
    registry = request.app.state.registry
    snapshot = registry.health_snapshot()

    missing = [d for d in settings.required_domains if d not in snapshot or not registry.get(d).loaded]
    unhealthy = [
        d
        for d in settings.required_domains
        if d in snapshot and d not in missing and snapshot[d].status != OperationalStatus.SUCCEEDED
    ]
    if missing or unhealthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "status": "not_ready",
            "missing_required_domains": missing,
            "unhealthy_required_domains": unhealthy,
        }

    return {
        "status": "ready",
        "domains": {name: report.status.value for name, report in snapshot.items()},
    }
