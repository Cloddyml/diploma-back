import redis.asyncio as redis


class RedisManager:
    _redis: redis.Redis  # pyright: ignore[reportUninitializedInstanceVariable]

    def __init__(self, host: str, port: int):
        self.host: str = host
        self.port: int = port

    async def connect(self):
        self._redis = redis.Redis(
            host=self.host,
            port=self.port,
            db=0,
        )

    @property
    def client(self) -> redis.Redis:
        return self._redis

    async def set(self, key: str, value: str, expire: int | None = None):
        if expire is not None:
            await self._redis.set(key, value, ex=expire)
        else:
            await self._redis.set(key, value)

    async def get(self, key: str):  # pyright: ignore[reportAny]
        return await self._redis.get(key)  # pyright: ignore[reportAny]

    async def delete(self, key: str):
        await self._redis.delete(key)

    async def close(self):
        if self._redis:
            await self._redis.aclose()
