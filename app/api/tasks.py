from fastapi import APIRouter, Body, Path, status

from app.api.deps.database import DBDep
from app.exceptions.excs import TaskNotFoundException
from app.exceptions.http_excs import TaskNotFoundHTTPException
from app.schemas import (
    SUCCESS_RESPONSE,
    StatusResponse,
    TaskDto,
    TaskPublishedDto,
    TopicAddRequestDto,
    TopicDto,
    TopicPatchRequestDto,
    TopicPublishedDto,
    TopicPutRequestDto,
)
from app.services import TasksService
from app.utils.responses import generate_responses

router = APIRouter(prefix="/topics/{topic_slug}/tasks", tags=["Задания"])
admin_router = APIRouter(prefix="/topics/{topic_slug}/tasks", tags=["Для админстрации"])


@router.get(
    "/published",
    response_model=list[TaskPublishedDto],
    status_code=status.HTTP_200_OK,
    summary="Получение списка всех опубликованных заданий к теме",
    responses=generate_responses(
        TaskNotFoundHTTPException,
    ),
)
async def get_all_published_tasks_by_topic(
    db: DBDep,
    topic_slug: str = Path(
        description="Нужен slug темы",
        max_length=100,
    ),
):
    try:
        return await TasksService(db).get_all_published_tasks_by_topic(slug=topic_slug)
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException
