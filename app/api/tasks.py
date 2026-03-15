from fastapi import APIRouter, Body, Path, status

from app.api.deps.database import DBDep
from app.exceptions.excs import (
    CannotBeEmptyTaskException,
    EmptyUpdateTaskDataException,
    TaskAlreadyExistsException,
    TaskNotFoundException,
    TopicNotFoundException,
)
from app.exceptions.http_excs import (
    CannotBeEmptyTaskHTTPException,
    EmptyUpdateTaskDataHTTPException,
    TaskAlreadyExistsHTTPException,
    TaskNotFoundHTTPException,
    TopicNotFoundHTTPException,
)
from app.schemas import (
    SUCCESS_RESPONSE,
    StatusResponse,
    TaskAddRequestDto,
    TaskDto,
    TaskPatchRequestDto,
    TaskPublishedDto,
    TaskPutRequestDto,
)
from app.services import TasksService
from app.utils.responses import generate_responses

router = APIRouter(prefix="/topics/{topic_slug}/tasks", tags=["Задания"])
admin_router = APIRouter(
    prefix="/topics/{topic_slug}/tasks", tags=["Для администрации"]
)


@admin_router.get(
    "",
    response_model=list[TaskDto],
    status_code=status.HTTP_200_OK,
    summary="Получение списка всех заданий к теме",
    responses=generate_responses(
        TopicNotFoundHTTPException,
        TaskNotFoundHTTPException,
    ),
)
async def get_all_tasks_by_topic(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
):
    try:
        return await TasksService(db).get_all_tasks_by_topic(topic_slug=topic_slug)
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException


@router.get(
    "/published",
    response_model=list[TaskPublishedDto],
    status_code=status.HTTP_200_OK,
    summary="Получение списка всех опубликованных заданий к теме",
    responses=generate_responses(
        TopicNotFoundHTTPException,
        TaskNotFoundHTTPException,
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
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException


@admin_router.post(
    "",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Добавление нового задания к теме",
    responses=generate_responses(
        TopicNotFoundHTTPException,
        TaskAlreadyExistsHTTPException,
    ),
)
async def add_new_task(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
    task_data: TaskAddRequestDto = Body(
        openapi_examples={
            "1": {
                "summary": "Задание 1",
                "value": {
                    "title": "Сортировка пузырьком",
                    "description": "Реализуйте сортировку пузырьком",
                    "starter_code": "def bubble_sort(arr):\n    pass",
                    "order_index": 1,
                    "time_limit_sec": 10,
                    "memory_limit_mb": 128,
                    "is_published": False,
                },
            },
            "2": {
                "summary": "Задание 2",
                "value": {
                    "title": "Бинарный поиск",
                    "description": "Реализуйте бинарный поиск",
                    "starter_code": None,
                    "order_index": 2,
                    "time_limit_sec": 5,
                    "memory_limit_mb": 64,
                    "is_published": True,
                },
            },
        }
    ),
):
    try:
        await TasksService(db).add_task(topic_slug=topic_slug, task_data=task_data)
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except TaskAlreadyExistsException:
        raise TaskAlreadyExistsHTTPException
    return SUCCESS_RESPONSE


@admin_router.put(
    "/{task_id}",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Полное изменение существующего задания",
    responses=generate_responses(
        TopicNotFoundHTTPException,
        TaskNotFoundHTTPException,
        EmptyUpdateTaskDataHTTPException,
        CannotBeEmptyTaskHTTPException,
    ),
)
async def edit_task(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
    task_id: int = Path(description="ID задания", gt=0),
    task_data: TaskPutRequestDto = Body(
        openapi_examples={
            "1": {
                "summary": "Задание 1",
                "value": {
                    "title": "Сортировка пузырьком",
                    "description": "Реализуйте сортировку пузырьком",
                    "starter_code": "def bubble_sort(arr):\n    pass",
                    "order_index": 1,
                    "time_limit_sec": 10,
                    "memory_limit_mb": 128,
                    "is_published": True,
                },
            },
        }
    ),
):
    try:
        await TasksService(db).edit_task(
            task_id=task_id, topic_slug=topic_slug, task_data=task_data
        )
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except EmptyUpdateTaskDataException:
        raise EmptyUpdateTaskDataHTTPException
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException
    except CannotBeEmptyTaskException:
        raise CannotBeEmptyTaskHTTPException
    return SUCCESS_RESPONSE


@admin_router.patch(
    "/{task_id}",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Частичное обновление существующего задания",
    responses=generate_responses(
        TopicNotFoundHTTPException,
        TaskNotFoundHTTPException,
        EmptyUpdateTaskDataHTTPException,
        CannotBeEmptyTaskHTTPException,
    ),
)
async def partial_edit_task(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
    task_id: int = Path(description="ID задания", gt=0),
    task_data: TaskPatchRequestDto = Body(
        openapi_examples={
            "1": {
                "summary": "Задание 1",
                "value": {
                    "title": "Новое название",
                    "is_published": True,
                },
            },
        }
    ),
):
    try:
        await TasksService(db).partial_edit_task(
            task_id=task_id, topic_slug=topic_slug, task_data=task_data
        )
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except EmptyUpdateTaskDataException:
        raise EmptyUpdateTaskDataHTTPException
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException
    except CannotBeEmptyTaskException:
        raise CannotBeEmptyTaskHTTPException
    return SUCCESS_RESPONSE


@admin_router.delete(
    "/{task_id}",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Удаление существующего задания",
    responses=generate_responses(
        TaskNotFoundHTTPException,
    ),
)
async def delete_task(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
    task_id: int = Path(description="ID задания", gt=0),
):
    try:
        await TasksService(db).delete_task(task_id=task_id)
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException
    return SUCCESS_RESPONSE
