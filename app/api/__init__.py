from fastapi import APIRouter

from app.api.tasks import admin_router as admin_tasks_router
from app.api.tasks import router as tasks_router
from app.api.topics import admin_router as admin_topics_router
from app.api.topics import router as topics_router

routers: list[APIRouter] = [
    admin_topics_router,
    admin_tasks_router,
    topics_router,
    tasks_router,
]
