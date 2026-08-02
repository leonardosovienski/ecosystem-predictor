"""Aggregator-owned Redis client. Per docs/adr/0002-data-ownership.md, this
Redis is for the aggregator's own short-lived dispatch/rate-limit state
only - never a shared cache between domains, and never a substitute for a
domain's own Redis (brasileirao-predictor's kernel/worker coordination
Redis, for example, is separate and unaffected by this one)."""

from __future__ import annotations

from dataclasses import dataclass

import redis.asyncio as redis

from ecosystem.settings import Settings


@dataclass
class CacheClient:
    _client: redis.Redis

    @classmethod
    def from_settings(cls, settings: Settings) -> CacheClient:
        return cls(_client=redis.from_url(settings.redis_url, decode_responses=True))

    async def ping(self) -> bool:
        return bool(await self._client.ping())

    async def set(self, key: str, value: str, *, ttl_seconds: int | None = None) -> None:
        await self._client.set(key, value, ex=ttl_seconds)

    async def get(self, key: str) -> str | None:
        return await self._client.get(key)

    async def delete(self, key: str) -> None:
        await self._client.delete(key)

    async def close(self) -> None:
        await self._client.aclose()
