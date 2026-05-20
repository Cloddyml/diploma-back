from fastapi import APIRouter, Path, status

from app.api.deps.database import DBDep
from app.exceptions.excs import TaskNotFoundException, TopicNotFoundException
from app.exceptions.http_excs import (
    TaskNotFoundHTTPException,
    TopicNotFoundHTTPException,
)
from app.schemas import TaskTestDto
from app.services import TaskTestsService
from app.utils.responses import generate_responses

router = APIRouter(
    prefix="/topics/{topic_slug}/tasks/{task_id}/tests", tags=["Тесты к заданиям"]
)


@router.get(
    "/visible",
    response_model=list[TaskTestDto],
    status_code=status.HTTP_200_OK,
    summary="Получение списка видимых тестов к заданию",
    responses=generate_responses(
        TopicNotFoundHTTPException,
        TaskNotFoundHTTPException,
    ),
)
async def get_visible_tests_by_task(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
    task_id: int = Path(description="ID задания", gt=0),
):
    try:
        return await TaskTestsService(db).get_visible_tests_by_task(
            topic_slug=topic_slug, task_id=task_id
        )
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException
