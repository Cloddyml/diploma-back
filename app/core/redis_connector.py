import redis.asyncio as redis


class RedisManager:
    _redis: redis.Redis

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def connect(self):
        self._redis = await redis.Redis(
            host=self.host,
            port=self.port,
        )

    @property
    def client(self) -> redis.Redis:
        return self._redis

    async def set(self, key: str, value: str, expire: int | None = None):
        if expire is not None:
            await self._redis.set(key, value, ex=expire)
        else:
            await self._redis.set(key, value)

    async def get(self, key: str):
        return await self._redis.get(key)

    async def delete(self, key: str):
        await self._redis.delete(key)

    async def close(self):
        if self._redis:
            await self._redis.aclose()
