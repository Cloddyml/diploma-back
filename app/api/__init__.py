from fastapi import APIRouter

from app.api.ai_interactions import router as ai_interactions_router
from app.api.progress import router as progress_router
from app.api.submissions import router as submissions_router
from app.api.task_tests import router as task_tests_router
from app.api.tasks import router as tasks_router
from app.api.topics import router as topics_router

routers: list[APIRouter] = [
    topics_router,
    tasks_router,
    task_tests_router,
    submissions_router,
    ai_interactions_router,
    progress_router,
]
