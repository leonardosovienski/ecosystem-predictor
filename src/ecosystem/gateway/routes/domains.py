"""Domain dispatch routes. Every route here fails closed: a domain that
isn't registered, isn't loaded, or doesn't implement the requested
capability returns 503/404 rather than a best-effort guess."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status

from ecosystem.contracts import (
    CapabilityManifest,
    HealthReport,
    OperationalStatus,
    PredictionRequest,
    PredictionResponse,
)
from ecosystem.gateway.auth import Principal, require_scope

router = APIRouter(prefix="/v1", tags=["domains"])


@router.get("/domains", response_model=list[str])
def list_domains(request: Request, _: Principal = Depends(require_scope("domains:read"))) -> list[str]:
    return request.app.state.registry.list_domains()


@router.get("/domains/{domain}/health", response_model=HealthReport)
def domain_health(
    domain: str, request: Request, _: Principal = Depends(require_scope("domains:read"))
) -> HealthReport:
    registry = request.app.state.registry
    record = registry.get(domain)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"unknown domain: {domain}")
    return registry.health_snapshot()[domain]


@router.get("/domains/{domain}/capabilities", response_model=CapabilityManifest)
def domain_capabilities(
    domain: str, request: Request, _: Principal = Depends(require_scope("domains:read"))
) -> CapabilityManifest:
    registry = request.app.state.registry
    record = registry.get(domain)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"unknown domain: {domain}")
    return registry.capability_snapshot()[domain]


@router.post("/domains/{domain}/predict", response_model=PredictionResponse)
def domain_predict(
    domain: str,
    body: dict,
    request: Request,
    _: Principal = Depends(require_scope("domains:predict")),
) -> PredictionResponse:
    registry = request.app.state.registry
    record = registry.get(domain)
    if record is None or not record.loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"domain unavailable: {domain}"
        )
    capabilities = registry.capability_snapshot().get(domain)
    if capabilities is None or not capabilities.supports_prediction:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"domain {domain!r} does not support prediction",
        )
    if not hasattr(record.instance, "predict"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"domain {domain!r} does not implement predict()",
        )

    run_id = uuid.uuid4().hex
    req = PredictionRequest(domain=domain, run_id=run_id, payload=body)
    try:
        raw = record.instance.predict(req.payload)  # type: ignore[union-attr]
    except Exception as exc:  # noqa: BLE001 - a domain error must not become an unhandled 500 with a stack trace leak
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    return PredictionResponse(
        domain=domain, run_id=run_id, status=OperationalStatus.SUCCEEDED, payload=raw or {}
    )
