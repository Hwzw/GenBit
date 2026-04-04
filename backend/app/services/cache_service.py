"""Redis caching wrapper with configurable TTL per resource type."""

import json

import redis.asyncio as aioredis

# Default TTLs in seconds
TTL_GENE = 86400  # 24 hours
TTL_PROTEIN = 86400
TTL_ORGANISM = 604800  # 7 days
TTL_CODON_TABLE = 604800


class CacheService:
    def __init__(self, redis_client: aioredis.Redis):
        self.redis = redis_client

    async def get_cached(self, key: str) -> dict | None:
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def set_cached(self, key: str, value: dict, ttl: int = TTL_GENE) -> None:
        await self.redis.set(key, json.dumps(value), ex=ttl)

    async def invalidate(self, key: str) -> None:
        await self.redis.delete(key)

    @staticmethod
    def make_key(resource_type: str, identifier: str) -> str:
        return f"genbit:{resource_type}:{identifier}"
