import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import redis_manager
from app.core.ai_client import ai_client
from app.core.config import settings
from app.core.database import engine
from app.core.database_celery import sync_engine
from app.core.logging import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Starting application (mode=%s)", settings.MODE)

    try:
        await ai_client.chat.completions.create(
            model=settings.QWEN_MODEL,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1,
        )
        logger.info("Qwen AI ping OK (model=%s)", settings.QWEN_MODEL)
    except Exception as ex:
        logger.warning("Qwen AI ping failed: %s", ex)

    await redis_manager.connect()
    logger.info("Redis connected (%s:%s)", settings.REDIS_HOST, settings.REDIS_PORT)

    yield

    await engine.dispose()
    sync_engine.dispose()
    await redis_manager.close()
    logger.info("Application stopped")
