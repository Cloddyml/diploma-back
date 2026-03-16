from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app import redis_manager
from app.core.ai_client import ai_client
from app.core.config import settings
from app.core.database import engine
from app.core.database_celery import sync_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await ai_client.chat.completions.create(
            model=settings.QWEN_MODEL,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1,
        )
    except Exception:
        pass
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.client), prefix="fastapi-cache")  # pyright: ignore[reportArgumentType]
    yield
    await engine.dispose()
    sync_engine.dispose()
    await redis_manager.close()
