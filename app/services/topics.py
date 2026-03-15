from app.models import TopicsOrm
from app.schemas import TopicAddRequestDto
from app.schemas.topics import TopicDto, TopicPublishedDto
from app.services.base import BaseService
from app.utils.schema_validation import validate_schema


class TopicsService(BaseService):
    async def get_all_topics(self) -> list[TopicDto]:
        return await self.db.topics.get_all()

    async def get_all_published_topics(self) -> list[TopicPublishedDto]:
        topics = await self.db.topics.get_filtered(TopicsOrm.is_published)
        return [validate_schema(topic, TopicPublishedDto) for topic in topics]

    async def add_topic(self, topic_data: TopicAddRequestDto):
        await self.db.topics.add(topic_data)
        await self.db.commit()
