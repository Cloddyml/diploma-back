from fastapi import APIRouter, Body, Path, Query, status

from app.api.deps.database import DBDep
from app.exceptions.excs import TopicNotFoundException
from app.exceptions.http_excs import TopicNotFoundHTTPException
from app.schemas import (
    SUCCESS_RESPONSE,
    StatusResponse,
    TopicProgressPatchDto,
    TopicPublishedDto,
)
from app.services import TopicsService
from app.utils.responses import generate_responses

router = APIRouter(prefix="/topics", tags=["Темы"])


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
