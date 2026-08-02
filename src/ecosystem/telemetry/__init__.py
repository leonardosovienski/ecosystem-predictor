"""OpenTelemetry wiring. If no OTLP endpoint is configured, spans/metrics
are still created (so instrumented code never branches on "is telemetry
on?") but exported nowhere - this is a deliberate no-op export, not a
silent failure: it's logged once at startup so it's visible in readiness
evidence."""

from __future__ import annotations

import logging

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from ecosystem.settings import Settings

logger = logging.getLogger("ecosystem.telemetry")


def configure_tracing(settings: Settings) -> TracerProvider:
    """Idempotent by design: OpenTelemetry's global tracer provider can only
    be set once per process (a second call is a silent no-op upstream, with
    a background exporter thread left dangling from whichever provider
    "lost"). A real gateway only calls this once at startup; a test suite
    that creates multiple app instances in one process must not each try to
    become *the* global provider, or a torn-down test's exporter can still
    be flushing into a closed stream when a later test's spans fire."""
    existing = trace.get_tracer_provider()
    if isinstance(existing, TracerProvider):
        return existing

    provider = TracerProvider(resource=Resource.create({SERVICE_NAME: settings.otel_service_name}))
    if settings.otel_exporter_otlp_endpoint:
        exporter = OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_endpoint)
        provider.add_span_processor(BatchSpanProcessor(exporter))
    else:
        logger.warning(
            "ECOSYSTEM_OTEL_EXPORTER_OTLP_ENDPOINT unset - traces are created but exported nowhere"
        )
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    return provider
