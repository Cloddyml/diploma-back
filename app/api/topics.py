from fastapi import APIRouter, status

from app.api.deps.database import DBDep
from app.schemas.topics import TopicDto, TopicPublishedDto
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
