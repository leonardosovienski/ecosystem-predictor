"""Real async Redis command behavior via fakeredis (an in-process Redis
simulator), not a hand-rolled mock of redis.asyncio's own interface - this
exercises the actual request/response shapes CacheClient depends on."""

from __future__ import annotations

import fakeredis
import pytest

from ecosystem.cache import CacheClient


@pytest.fixture
async def cache() -> CacheClient:
    client = CacheClient(_client=fakeredis.FakeAsyncRedis(decode_responses=True))
    yield client
    await client.close()


async def test_ping(cache: CacheClient):
    assert await cache.ping() is True


async def test_set_get_round_trip(cache: CacheClient):
    await cache.set("dispatch:run-1", "in-flight")

    assert await cache.get("dispatch:run-1") == "in-flight"


async def test_get_missing_key_is_none(cache: CacheClient):
    assert await cache.get("does-not-exist") is None


async def test_delete_removes_key(cache: CacheClient):
    await cache.set("k", "v")
    await cache.delete("k")

    assert await cache.get("k") is None


async def test_set_with_ttl_expires(cache: CacheClient):
    await cache.set("short-lived", "v", ttl_seconds=1)

    assert await cache.get("short-lived") == "v"
    ttl = await cache._client.ttl("short-lived")
    assert 0 < ttl <= 1
