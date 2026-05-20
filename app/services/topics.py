from datetime import datetime, timezone

from app.exceptions.excs import ObjectNotFoundException, TopicNotFoundException
from app.models import TopicsOrm
from app.schemas import (
    TopicProgressPatchDto,
    TopicProgressUpdateDto,
    TopicPublishedDto,
)
from app.services.base import BaseService
from app.utils.schema_validation import validate_schema


class TopicsService(BaseService):
    async def get_all_published_topics(
        self, is_interview: bool | None = None
    ) -> list[TopicPublishedDto]:
        filter_by: dict[str, bool] = {}
        if is_interview is not None:
            filter_by["is_interview"] = is_interview
        topics = await self.db.topics.get_filtered(TopicsOrm.is_published, **filter_by)
        return [validate_schema(topic, TopicPublishedDto) for topic in topics]

    async def get_published_topic_by_slug(self, slug: str) -> TopicPublishedDto:
        topic = await self.db.topics.get_one_or_none(slug=slug, is_published=True)
        if topic is None:
            raise TopicNotFoundException
        return validate_schema(topic, TopicPublishedDto)

    async def mark_topic_completion(
        self, topic_slug: str, data: TopicProgressPatchDto
    ) -> None:
        topic = await self.db.topics.get_one_or_none(
            slug=topic_slug, is_published=True
        )
        if topic is None:
            raise TopicNotFoundException

        update_dto = TopicProgressUpdateDto(
            is_completed=data.is_completed,
            completed_at=datetime.now(timezone.utc) if data.is_completed else None,
        )

        try:
            await self.db.topics.edit(id=topic.id, data=update_dto, exclude_unset=False)
            await self.db.commit()
        except ObjectNotFoundException as ex:
            raise TopicNotFoundException from ex
