"""Real S3 API behavior via moto (an in-process S3 simulator), not a
hand-rolled mock of boto3's own interface - this exercises the actual
request/response shapes ObjectStorage depends on."""

from __future__ import annotations

import boto3
import pytest
from moto import mock_aws

from ecosystem.settings import Settings
from ecosystem.storage import ObjectStorage


@pytest.fixture
def storage_settings() -> Settings:
    return Settings(
        jwt_secret="test-secret-at-least-32-bytes-long-xx",  # gitleaks:allow
        database_url="postgresql+asyncpg://t:t@localhost/t",
        redis_url="redis://localhost/0",
        object_storage_bucket="ecosystem-test-bucket",
        object_storage_access_key="testing",
        object_storage_secret_key="testing",
    )


@mock_aws
def test_put_get_round_trip(storage_settings: Settings):
    boto3.client("s3", region_name="us-east-1").create_bucket(Bucket=storage_settings.object_storage_bucket)
    storage = ObjectStorage.from_settings(storage_settings)

    storage.put("runs/abc.json", b'{"ok": true}', content_type="application/json")

    assert storage.get("runs/abc.json") == b'{"ok": true}'


@mock_aws
def test_exists_is_false_for_a_missing_key(storage_settings: Settings):
    boto3.client("s3", region_name="us-east-1").create_bucket(Bucket=storage_settings.object_storage_bucket)
    storage = ObjectStorage.from_settings(storage_settings)

    assert storage.exists("does/not/exist.json") is False


@mock_aws
def test_exists_is_true_after_put(storage_settings: Settings):
    boto3.client("s3", region_name="us-east-1").create_bucket(Bucket=storage_settings.object_storage_bucket)
    storage = ObjectStorage.from_settings(storage_settings)
    storage.put("a.txt", b"hi")

    assert storage.exists("a.txt") is True


def test_from_settings_fails_closed_without_a_bucket():
    settings = Settings(
        jwt_secret="test-secret-at-least-32-bytes-long-xx",  # gitleaks:allow
        database_url="postgresql+asyncpg://t:t@localhost/t",
        redis_url="redis://localhost/0",
        object_storage_bucket="",
    )
    with pytest.raises(RuntimeError, match="required"):
        ObjectStorage.from_settings(settings)
