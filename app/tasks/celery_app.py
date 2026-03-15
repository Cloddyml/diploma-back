from celery import Celery

from app.core.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_BROKER_URL,
    include=[
        "app.tasks.tasks",
    ],
)
