from __future__ import annotations

import pytest
from pydantic import ValidationError

from ecosystem.settings import Settings


def test_missing_required_secrets_fail_closed(monkeypatch):
    monkeypatch.delenv("ECOSYSTEM_JWT_SECRET", raising=False)
    monkeypatch.delenv("ECOSYSTEM_DATABASE_URL", raising=False)
    monkeypatch.delenv("ECOSYSTEM_REDIS_URL", raising=False)
    monkeypatch.delenv("ECOSYSTEM_OBJECT_STORAGE_BUCKET", raising=False)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)  # type: ignore[call-arg]


def test_csv_env_vars_split_into_lists():
    settings = Settings(
        jwt_secret="s",
        database_url="postgresql+asyncpg://u:p@h/db",
        redis_url="redis://h/0",
        object_storage_bucket="b",
        cors_allow_origins="https://a.example,https://b.example",
        required_domains="f1,cs",
    )
    assert settings.cors_allow_origins == ["https://a.example", "https://b.example"]
    assert settings.required_domains == ["f1", "cs"]
