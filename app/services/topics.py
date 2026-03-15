from app.models import TopicsOrm
from app.schemas.topics import TopicDto, TopicPublishedDto
from app.services.base import BaseService


class TopicsService(BaseService):
    async def get_all_topics(self) -> list[TopicDto]:
        return await self.db.topics.get_all()

    async def get_all_published_topics(self) -> list[TopicPublishedDto]:
        topics = await self.db.topics.get_filtered(TopicsOrm.is_published)
        return [
            TopicPublishedDto.model_validate(topic.model_dump()) for topic in topics
        ]
