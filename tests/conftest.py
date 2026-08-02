from __future__ import annotations

import jwt
import pytest
from opentelemetry import trace

from ecosystem.settings import Settings


@pytest.fixture(scope="session", autouse=True)
def _shutdown_tracer_provider_before_interpreter_teardown():
    """configure_tracing() (ecosystem.telemetry) registers exactly one
    global TracerProvider for the whole test session (it's idempotent - see
    that module's docstring). Its BatchSpanProcessor runs a background
    flush thread; without an explicit shutdown, that thread can still be
    writing to stdout when the interpreter starts closing streams at exit,
    which prints a spurious "I/O operation on closed file" traceback after
    the test result summary. Shutting it down here, once, after every test
    has run, avoids that without touching the module's real
    once-per-process semantics."""
    yield
    provider = trace.get_tracer_provider()
    shutdown = getattr(provider, "shutdown", None)
    if callable(shutdown):
        shutdown()


@pytest.fixture
def settings() -> Settings:
    return Settings(
        jwt_secret="test-secret-at-least-32-bytes-long-xx",  # noqa: S106 - test fixture, not a real credential  # gitleaks:allow
        database_url="postgresql+asyncpg://test:test@localhost:5432/test",
        redis_url="redis://localhost:6379/0",
        object_storage_bucket="test-bucket",
        required_domains=[],
    )


@pytest.fixture
def token_factory(settings: Settings):
    def _make(subject: str = "test-user", scopes: str = "domains:read domains:predict") -> str:
        return jwt.encode(
            {"sub": subject, "scope": scopes, "aud": settings.jwt_audience},
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )

    return _make
