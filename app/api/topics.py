from fastapi import APIRouter, Body, status

from app.api.deps.database import DBDep
from app.schemas import (
    SUCCESS_RESPONSE,
    StatusResponse,
    TopicAddRequestDto,
    TopicDto,
    TopicPublishedDto,
)
from app.services import TopicsService

router = APIRouter(prefix="/topics", tags=["Темы"])


@router.get(
    "",
    response_model=list[TopicDto],
    status_code=status.HTTP_200_OK,
    summary="Получение списка всех тем",
    tags=["Для админстрации"],
)
async def get_all_topics(db: DBDep):
    return await TopicsService(db).get_all_topics()


@router.get(
    "_published",
    response_model=list[TopicPublishedDto],
    status_code=status.HTTP_200_OK,
    summary="Получение списка всех опубликованных тем",
)
async def get_all_published_topics(db: DBDep):
    return await TopicsService(db).get_all_published_topics()


@router.post(
    "",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Добавление новой темы",
    tags=["Для админстрации"],
)
async def add_new_topic(
    db: DBDep,
    topic_data: TopicAddRequestDto = Body(
        openapi_examples={
            "1": {
                "summary": "Тема 1",
                "value": {
                    "slug": "pytorch",
                    "title": "Библиотека PyTorch",
                    "content": "",
                    "order_index": 1,
                    "is_published": False,
                },
            },
            "2": {
                "summary": "Тема 2",
                "value": {
                    "slug": "Pandas",
                    "title": "Библиотека Pandas",
                    "content": "",
                    "order_index": 2,
                    "is_published": True,
                },
            },
        }
    ),
):
    await TopicsService(db).add_topic(topic_data)
    return SUCCESS_RESPONSE
