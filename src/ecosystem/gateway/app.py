"""FastAPI application factory. All cross-cutting concerns (CORS, auth,
telemetry, registry lifecycle) are wired here, once - domain routes stay
free of infrastructure code."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from ecosystem.gateway.routes import domains, health
from ecosystem.registry import Registry
from ecosystem.settings import Settings, get_settings
from ecosystem.telemetry import configure_tracing


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.settings = settings
        app.state.registry = Registry.discover(group=settings.plugin_group)
        configure_tracing(settings)
        yield

    app = FastAPI(title="ecosystem-predictor gateway", version="0.1.0", lifespan=lifespan)
    # Every dependency that needs Settings must resolve to this exact instance -
    # otherwise a caller-provided settings object (e.g. a test double) is
    # silently ignored by anything using Depends(get_settings), which would
    # instead re-parse from the real environment.
    app.dependency_overrides[get_settings] = lambda: settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )

    app.include_router(health.router)
    app.include_router(domains.router)

    FastAPIInstrumentor.instrument_app(app)
    return app
