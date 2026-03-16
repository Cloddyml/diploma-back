from celery import Celery

from app.core.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_BROKER_URL,
    include=["app.tasks.tasks"],
)

celery_instance.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    task_time_limit=300,
    task_soft_time_limit=280,
    worker_max_tasks_per_child=100,
)
