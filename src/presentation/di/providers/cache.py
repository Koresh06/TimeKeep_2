from dishka import Scope, provide, Provider
from redis.asyncio import Redis

from src.core.config.redis import RedisSettings
from src.domain.interfaces.cache import ICache
from src.infrastructure.cache.redis import RedisCache


class CacheProvider(Provider):

    @provide(scope=Scope.APP)
    def get_redis_client(self, settings: RedisSettings) -> Redis:
        return Redis.from_url(settings.url)

    @provide(scope=Scope.APP, provides=ICache)
    def get_cache(self, redis: Redis) -> ICache:
        return RedisCache(redis)