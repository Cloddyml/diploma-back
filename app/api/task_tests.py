from fastapi import APIRouter, Body, Path, status

from app.api.deps.database import DBDep
from app.exceptions.excs import (
    CannotBeEmptyTaskTestException,
    EmptyUpdateTaskTestDataException,
    TaskNotFoundException,
    TaskTestAlreadyExistsException,
    TaskTestNotFoundException,
    TopicNotFoundException,
)
from app.exceptions.http_excs import (
    CannotBeEmptyTaskTestHTTPException,
    EmptyUpdateTaskTestDataHTTPException,
    TaskNotFoundHTTPException,
    TaskTestAlreadyExistsHTTPException,
    TaskTestNotFoundHTTPException,
    TopicNotFoundHTTPException,
)
from app.schemas import (
    SUCCESS_RESPONSE,
    StatusResponse,
    TaskTestAddRequestDto,
    TaskTestDto,
    TaskTestPatchRequestDto,
    TaskTestPutRequestDto,
)
from app.services import TaskTestsService
from app.utils.responses import generate_responses

router = APIRouter(
    prefix="/topics/{topic_slug}/tasks/{task_id}/tests", tags=["Тесты к заданиям"]
)
admin_router = APIRouter(
    prefix="/topics/{topic_slug}/tasks/{task_id}/tests",
    tags=["Для администрации - тесты"],
)


@admin_router.get(
    "",
    response_model=list[TaskTestDto],
    status_code=status.HTTP_200_OK,
    summary="Получение списка всех тестов к заданию",
    responses=generate_responses(
        TopicNotFoundHTTPException,
        TaskNotFoundHTTPException,
    ),
)
async def get_all_tests_by_task(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
    task_id: int = Path(description="ID задания", gt=0),
):
    try:
        return await TaskTestsService(db).get_all_tests_by_task(
            topic_slug=topic_slug, task_id=task_id
        )
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException


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


@admin_router.post(
    "",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Добавление нового теста к заданию",
    responses=generate_responses(
        TopicNotFoundHTTPException,
        TaskNotFoundHTTPException,
        TaskTestAlreadyExistsHTTPException,
    ),
)
async def add_new_test(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
    task_id: int = Path(description="ID задания", gt=0),
    test_data: TaskTestAddRequestDto = Body(
        openapi_examples={
            "1": {
                "summary": "Открытый тест",
                "value": {
                    "test_code": "assert bubble_sort([3, 1, 2]) == [1, 2, 3]",
                    "is_hidden": False,
                    "order_index": 1,
                },
            },
            "2": {
                "summary": "Скрытый тест",
                "value": {
                    "test_code": "assert bubble_sort([]) == []",
                    "is_hidden": True,
                    "order_index": 2,
                },
            },
        }
    ),
):
    try:
        await TaskTestsService(db).add_test(
            topic_slug=topic_slug, task_id=task_id, test_data=test_data
        )
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException
    except TaskTestAlreadyExistsException:
        raise TaskTestAlreadyExistsHTTPException
    return SUCCESS_RESPONSE


@admin_router.put(
    "/{test_id}",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Полное обновление существующего теста",
    responses=generate_responses(
        TopicNotFoundHTTPException,
        TaskNotFoundHTTPException,
        TaskTestNotFoundHTTPException,
        EmptyUpdateTaskTestDataHTTPException,
        CannotBeEmptyTaskTestHTTPException,
    ),
)
async def edit_test(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
    task_id: int = Path(description="ID задания", gt=0),
    test_id: int = Path(description="ID теста", gt=0),
    test_data: TaskTestPutRequestDto = Body(
        openapi_examples={
            "1": {
                "summary": "Обновлённый тест",
                "value": {
                    "test_code": "assert bubble_sort([5, 3, 1]) == [1, 3, 5]",
                    "is_hidden": False,
                    "order_index": 1,
                },
            },
        }
    ),
):
    try:
        await TaskTestsService(db).edit_test(
            topic_slug=topic_slug,
            task_id=task_id,
            test_id=test_id,
            test_data=test_data,
        )
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException
    except TaskTestNotFoundException:
        raise TaskTestNotFoundHTTPException
    except EmptyUpdateTaskTestDataException:
        raise EmptyUpdateTaskTestDataHTTPException
    except CannotBeEmptyTaskTestException:
        raise CannotBeEmptyTaskTestHTTPException
    return SUCCESS_RESPONSE


@admin_router.patch(
    "/{test_id}",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Частичное обновление существующего теста",
    responses=generate_responses(
        TopicNotFoundHTTPException,
        TaskNotFoundHTTPException,
        TaskTestNotFoundHTTPException,
        EmptyUpdateTaskTestDataHTTPException,
        CannotBeEmptyTaskTestHTTPException,
    ),
)
async def partial_edit_test(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
    task_id: int = Path(description="ID задания", gt=0),
    test_id: int = Path(description="ID теста", gt=0),
    test_data: TaskTestPatchRequestDto = Body(
        openapi_examples={
            "1": {
                "summary": "Скрыть тест",
                "value": {
                    "is_hidden": True,
                },
            },
            "2": {
                "summary": "Обновить код теста",
                "value": {
                    "test_code": "assert bubble_sort([2, 2, 1]) == [1, 2, 2]",
                },
            },
        }
    ),
):
    try:
        await TaskTestsService(db).partial_edit_test(
            topic_slug=topic_slug,
            task_id=task_id,
            test_id=test_id,
            test_data=test_data,
        )
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException
    except TaskTestNotFoundException:
        raise TaskTestNotFoundHTTPException
    except EmptyUpdateTaskTestDataException:
        raise EmptyUpdateTaskTestDataHTTPException
    except CannotBeEmptyTaskTestException:
        raise CannotBeEmptyTaskTestHTTPException
    return SUCCESS_RESPONSE


@admin_router.delete(
    "/{test_id}",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Удаление существующего теста",
    responses=generate_responses(
        TopicNotFoundHTTPException,
        TaskNotFoundHTTPException,
        TaskTestNotFoundHTTPException,
    ),
)
async def delete_test(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
    task_id: int = Path(description="ID задания", gt=0),
    test_id: int = Path(description="ID теста", gt=0),
):
    try:
        await TaskTestsService(db).delete_test(
            topic_slug=topic_slug, task_id=task_id, test_id=test_id
        )
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except TaskNotFoundException:
        raise TaskNotFoundHTTPException
    except TaskTestNotFoundException:
        raise TaskTestNotFoundHTTPException
    return SUCCESS_RESPONSE
