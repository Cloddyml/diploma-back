from app.exceptions.excs import (
    CannotBeEmptyException,
    CannotBeEmptyTopicException,
    EmptyUpdateDataException,
    EmptyUpdateTopicDataException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    TopicAlreadyExistsException,
    TopicNotFoundException,
)
from app.models import TopicsOrm
from app.schemas import (
    TopicAddRequestDto,
    TopicDto,
    TopicPatchRequestDto,
    TopicPublishedDto,
    TopicPutRequestDto,
)
from app.services.base import BaseService
from app.utils.schema_validation import validate_schema


class TopicsService(BaseService):
    async def get_all_topics(self) -> list[TopicDto]:
        return await self.db.topics.get_all()

    async def get_all_published_topics(self) -> list[TopicPublishedDto]:
        topics = await self.db.topics.get_filtered(TopicsOrm.is_published)
        return [validate_schema(topic, TopicPublishedDto) for topic in topics]

    async def get_published_topic_by_slug(self, slug: str) -> TopicPublishedDto:
        topic = await self.db.topics.get_one_or_none(slug=slug, is_published=True)
        if topic is None:
            raise TopicNotFoundException
        return validate_schema(topic, TopicPublishedDto)

    async def add_topic(self, topic_data: TopicAddRequestDto):
        try:
            await self.db.topics.add(topic_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise TopicAlreadyExistsException from ex

    async def edit_topic(
        self,
        topic_id: int,
        topic_data: TopicPutRequestDto,
    ):
        try:
            await self.db.topics.edit(id=topic_id, data=topic_data)
            await self.db.commit()
        except EmptyUpdateDataException as ex:
            raise EmptyUpdateTopicDataException from ex
        except ObjectNotFoundException as ex:
            raise TopicNotFoundException from ex
        except CannotBeEmptyException as ex:
            raise CannotBeEmptyTopicException from ex

    async def partial_edit_topic(
        self,
        topic_id: int,
        topic_data: TopicPatchRequestDto,
    ):
        try:
            await self.db.topics.edit(id=topic_id, data=topic_data, exclude_unset=True)
            await self.db.commit()
        except EmptyUpdateDataException as ex:
            raise EmptyUpdateTopicDataException from ex
        except ObjectNotFoundException as ex:
            raise TopicNotFoundException from ex
        except CannotBeEmptyException as ex:
            raise CannotBeEmptyTopicException from ex

    async def delete_topic(self, topic_id: int):
        try:
            await self.db.topics.delete(id=topic_id)
            await self.db.commit()
        except ObjectNotFoundException as ex:
            raise TopicNotFoundException from ex
