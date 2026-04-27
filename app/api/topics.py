from fastapi import APIRouter, Body, Path, Query, status
from fastapi_cache.decorator import cache

from app.api.deps.database import DBDep
from app.exceptions.excs import (
    CannotBeEmptyTopicException,
    EmptyUpdateTopicDataException,
    TopicAlreadyExistsException,
    TopicNotFoundException,
)
from app.exceptions.http_excs import (
    CannotBeEmptyTopicHTTPException,
    EmptyUpdateTopicDataHTTPException,
    TopicAlreadyExistsHTTPException,
    TopicNotFoundHTTPException,
)
from app.schemas import (
    SUCCESS_RESPONSE,
    StatusResponse,
    TopicAddRequestDto,
    TopicDto,
    TopicPatchRequestDto,
    TopicProgressPatchDto,
    TopicPublishedDto,
    TopicPutRequestDto,
)
from app.services import TopicsService
from app.utils.responses import generate_responses

router = APIRouter(prefix="/topics", tags=["Темы"])
admin_router = APIRouter(prefix="/topics", tags=["Для администрации - темы"])


@admin_router.get(
    "",
    response_model=list[TopicDto],
    status_code=status.HTTP_200_OK,
    summary="Получение списка всех тем",
)
@cache(expire=10)
async def get_all_topics(db: DBDep) -> list[TopicDto]:
    print("Иду в БД")
    return await TopicsService(db).get_all_topics()


@router.get(
    "/published",
    response_model=list[TopicPublishedDto],
    status_code=status.HTTP_200_OK,
    summary="Получение списка всех опубликованных тем",
)
async def get_all_published_topics(
    db: DBDep,
    is_interview: bool | None = Query(
        None,
        description="Фильтр: false — учебные темы, true — вопросы для собеседований",
    ),
):
    return await TopicsService(db).get_all_published_topics(is_interview=is_interview)


@router.get(
    "/{topic_slug}",
    response_model=TopicPublishedDto,
    status_code=status.HTTP_200_OK,
    summary="Получение опубликованной темы по slug",
    responses=generate_responses(
        TopicNotFoundHTTPException,
    ),
)
async def get_published_topic(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
):
    try:
        return await TopicsService(db).get_published_topic_by_slug(slug=topic_slug)
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException


@admin_router.post(
    "",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    responses=generate_responses(
        TopicAlreadyExistsHTTPException,
    ),
    summary="Добавление новой темы",
)
async def add_new_topic(
    db: DBDep,
    topic_data: TopicAddRequestDto = Body(
        openapi_examples={
            "1": {
                "summary": "Учебная тема",
                "value": {
                    "slug": "pytorch",
                    "title": "Библиотека PyTorch",
                    "content": "",
                    "order_index": 1,
                    "is_published": False,
                    "is_interview": False,
                },
            },
            "2": {
                "summary": "Тема для собеседований",
                "value": {
                    "slug": "interview-graphs",
                    "title": "Графы",
                    "content": "",
                    "order_index": 1,
                    "is_published": True,
                    "is_interview": True,
                },
            },
        }
    ),
):
    try:
        await TopicsService(db).add_topic(topic_data=topic_data)
    except TopicAlreadyExistsException:
        raise TopicAlreadyExistsHTTPException
    return SUCCESS_RESPONSE


@admin_router.put(
    "/{topic_id}",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    responses=generate_responses(
        TopicNotFoundHTTPException,
        EmptyUpdateTopicDataHTTPException,
        CannotBeEmptyTopicHTTPException,
    ),
    summary="Полное изменение существующей темы",
)
async def edit_topic(
    db: DBDep,
    topic_id: int = Path(description="ID темы", gt=0),
    topic_data: TopicPutRequestDto = Body(
        openapi_examples={
            "1": {
                "summary": "Тема 1",
                "value": {
                    "slug": "some-library",
                    "title": "Ещё библиотека",
                    "content": "",
                    "order_index": 6,
                    "is_published": True,
                    "is_interview": False,
                },
            },
        }
    ),
):
    try:
        await TopicsService(db).edit_topic(topic_id=topic_id, topic_data=topic_data)
    except EmptyUpdateTopicDataException:
        raise EmptyUpdateTopicDataHTTPException
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except CannotBeEmptyTopicException:
        raise CannotBeEmptyTopicHTTPException
    return SUCCESS_RESPONSE


@admin_router.patch(
    "/{topic_id}",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    responses=generate_responses(
        TopicNotFoundHTTPException,
        EmptyUpdateTopicDataHTTPException,
        CannotBeEmptyTopicHTTPException,
    ),
    summary="Частичное обновление существующей темы",
)
async def partial_edit_topic(
    db: DBDep,
    topic_id: int = Path(description="ID темы", gt=0),
    topic_data: TopicPatchRequestDto = Body(
        openapi_examples={
            "1": {
                "summary": "Тема 1",
                "value": {
                    "slug": "some-library",
                    "title": "Ещё библиотека",
                    "content": "",
                    "order_index": 6,
                    "is_published": True,
                },
            },
        }
    ),
):
    try:
        await TopicsService(db).partial_edit_topic(
            topic_id=topic_id, topic_data=topic_data
        )
    except EmptyUpdateTopicDataException:
        raise EmptyUpdateTopicDataHTTPException
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    except CannotBeEmptyTopicException:
        raise CannotBeEmptyTopicHTTPException
    return SUCCESS_RESPONSE


@admin_router.delete(
    "/{topic_id}",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    responses=generate_responses(
        TopicNotFoundHTTPException,
    ),
    summary="Удаление существующей темы",
)
async def delete_topic(
    db: DBDep,
    topic_id: int = Path(description="ID темы", gt=0),
):
    try:
        await TopicsService(db).delete_topic(topic_id=topic_id)
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    return SUCCESS_RESPONSE


@router.patch(
    "/{topic_slug}/progress",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Отметить тему как выполненную / невыполненную",
    responses=generate_responses(TopicNotFoundHTTPException),
)
async def mark_topic_completion(
    db: DBDep,
    topic_slug: str = Path(description="Slug темы", max_length=100),
    data: TopicProgressPatchDto = Body(
        openapi_examples={
            "1": {
                "summary": "Отметить как выполненную",
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
        await TopicsService(db).mark_topic_completion(topic_slug, data)
    except TopicNotFoundException:
        raise TopicNotFoundHTTPException
    return SUCCESS_RESPONSE
