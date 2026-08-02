"""Aggregator settings. Everything is env-driven (Pydantic Settings v2) —
no secret ever has a non-empty default. Fields with no safe default are
required; the process refuses to start rather than run half-configured."""

from __future__ import annotations

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ECOSYSTEM_", env_file=".env", extra="ignore")

    environment: str = "development"

    # --- auth / gateway ---
    jwt_secret: str = Field(..., description="HS256 signing secret; required, no default")
    jwt_algorithm: str = "HS256"
    jwt_audience: str = "ecosystem-predictor"
    cors_allow_origins: list[str] = Field(default_factory=list)

    # --- data plane ---
    database_url: str = Field(..., description="postgresql+asyncpg://... ; required, no default")
    redis_url: str = Field(..., description="redis://... ; required, no default")

    # --- object storage (S3-compatible) ---
    object_storage_endpoint_url: str | None = None
    object_storage_bucket: str = Field(..., description="required, no default")
    object_storage_access_key: str | None = None
    object_storage_secret_key: str | None = None

    # --- telemetry ---
    otel_service_name: str = "ecosystem-predictor"
    otel_exporter_otlp_endpoint: str | None = None

    # --- registry ---
    plugin_group: str = "predictor.plugins"
    required_domains: list[str] = Field(
        default_factory=list,
        description="Domains that MUST be loaded for /readyz to report ready. "
        "Empty means readiness never gates on domain availability - set this "
        "explicitly once real domain adapters exist.",
    )

    @field_validator("cors_allow_origins", "required_domains", mode="before")
    @classmethod
    def _split_csv(cls, value: object) -> object:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]  # required fields come from env/`.env`
