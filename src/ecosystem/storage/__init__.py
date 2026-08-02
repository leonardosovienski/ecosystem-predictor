"""S3-compatible object storage client. Fail-closed: constructing this
without a bucket configured raises immediately rather than deferring the
failure to the first upload."""

from __future__ import annotations

from dataclasses import dataclass
from typing import BinaryIO

import boto3

from ecosystem.settings import Settings


@dataclass
class ObjectStorage:
    bucket: str
    _client: object

    @classmethod
    def from_settings(cls, settings: Settings) -> ObjectStorage:
        if not settings.object_storage_bucket:
            raise RuntimeError("ECOSYSTEM_OBJECT_STORAGE_BUCKET is required - fail-closed, no default bucket")
        client = boto3.client(
            "s3",
            endpoint_url=settings.object_storage_endpoint_url,
            aws_access_key_id=settings.object_storage_access_key,
            aws_secret_access_key=settings.object_storage_secret_key,
        )
        return cls(bucket=settings.object_storage_bucket, _client=client)

    def put(
        self, key: str, body: bytes | BinaryIO, *, content_type: str = "application/octet-stream"
    ) -> None:
        self._client.put_object(Bucket=self.bucket, Key=key, Body=body, ContentType=content_type)  # type: ignore[attr-defined]

    def get(self, key: str) -> bytes:
        response = self._client.get_object(Bucket=self.bucket, Key=key)  # type: ignore[attr-defined]
        return response["Body"].read()

    def exists(self, key: str) -> bool:
        try:
            self._client.head_object(Bucket=self.bucket, Key=key)  # type: ignore[attr-defined]
            return True
        except Exception:  # noqa: BLE001 - boto3 raises a botocore ClientError subtype we don't want to import here
            return False
