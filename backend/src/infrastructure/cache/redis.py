import json
from dataclasses import dataclass
from datetime import datetime, date, time

from redis.asyncio import Redis

from src.domain.interfaces.cache import ICache


def _serialize(obj):
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


@dataclass(frozen=True)
class RedisCache(ICache):
    _redis: Redis

    async def get(self, key: str) -> dict | list | None:
        value = await self._redis.get(key)
        return json.loads(value) if value else None

    async def set(self, key: str, value: dict | list, ttl: int = 300) -> None:
        await self._redis.set(
            key,
            json.dumps(value, default=_serialize),
            ex=ttl,
        )

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)