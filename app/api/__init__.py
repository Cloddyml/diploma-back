from fastapi import APIRouter

from app.api.task_tests import admin_router as admin_task_tests_router
from app.api.task_tests import router as task_tests_router
from app.api.tasks import admin_router as admin_tasks_router
from app.api.tasks import router as tasks_router
from app.api.topics import admin_router as admin_topics_router
from app.api.topics import router as topics_router

routers: list[APIRouter] = [
    admin_topics_router,
    admin_tasks_router,
    admin_task_tests_router,
    topics_router,
    tasks_router,
    task_tests_router,
]
