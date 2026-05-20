from fastapi import APIRouter, Body, Path, status

from app.api.deps.database import DBDep
from app.exceptions.excs import TaskNotFoundException, TopicNotFoundException
from app.exceptions.http_excs import (
    TaskNotFoundHTTPException,
    TopicNotFoundHTTPException,
)
from app.schemas import (
    SUCCESS_RESPONSE,
    StatusResponse,
    TaskProgressPatchDto,
    TaskPublishedDto,
)
from app.services import TasksService
from app.utils.responses import generate_responses

router = APIRouter(prefix="/topics/{topic_slug}/tasks", tags=["Задания"])


@router.get(
    "/published",
    response_model=list[TaskPublishedDto],
    status_code=status.HTTP_200_OK,
    summary="Получение списка всех опубликованных заданий к теме",
    responses=generate_responses(
        TopicNotFoundHTTPException,
    ),
)
async def get_all_published_tasks_by_topic(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
):
    try:
        return await TasksService(db).get_all_published_tasks_by_topic(
            topic_slug=topic_slug
        )
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException


@router.get(
    "/{task_id}/published",
    response_model=TaskPublishedDto,
    status_code=status.HTTP_200_OK,
    summary="Получение опубликованного задания по ID",
    responses=generate_responses(
        TopicNotFoundHTTPException,
        TaskNotFoundHTTPException,
    ),
)
async def get_published_task(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
    task_id: int = Path(description="ID задания", gt=0),
):
    try:
        return await TasksService(db).get_published_task(
            topic_slug=topic_slug, task_id=task_id
        )
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException


@router.patch(
    "/{task_id}/progress",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Отметить задание как выполненное / невыполненное",
    responses=generate_responses(
        TopicNotFoundHTTPException,
        TaskNotFoundHTTPException,
    ),
)
async def mark_task_completion(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
    task_id: int = Path(description="ID задания", gt=0),
    data: TaskProgressPatchDto = Body(
        openapi_examples={
            "1": {
                "summary": "Отметить как выполненное",
                "value": {"is_completed": True},
            },
            "2": {
                "summary": "Снять отметку",
                "value": {"is_completed": False},
            },
        }
    ),
):
    try:
        await TasksService(db).mark_task_completion(topic_slug, task_id, data)
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException
    return SUCCESS_RESPONSE
