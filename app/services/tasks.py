from datetime import datetime, timezone

from app.exceptions.excs import (
    ObjectNotFoundException,
    TaskNotFoundException,
    TopicNotFoundException,
)
from app.schemas import (
    TaskProgressPatchDto,
    TaskProgressUpdateDto,
    TaskPublishedDto,
)
from app.services.base import BaseService
from app.utils.schema_validation import validate_schema


class TasksService(BaseService):
    async def _resolve_topic_id(self, topic_slug: str) -> int:
        topic = await self.db.topics.get_one_or_none(
            slug=topic_slug, is_published=True
        )
        if topic is None:
            raise TopicNotFoundException
        return topic.id

    async def get_all_published_tasks_by_topic(
        self, topic_slug: str
    ) -> list[TaskPublishedDto]:
        await self._resolve_topic_id(topic_slug)
        tasks = await self.db.tasks.get_published_tasks_by_topic_slug(slug=topic_slug)
        return [validate_schema(task, TaskPublishedDto) for task in tasks]

    async def get_published_task(
        self, topic_slug: str, task_id: int
    ) -> TaskPublishedDto:
        topic_id = await self._resolve_topic_id(topic_slug)
        task = await self.db.tasks.get_one_or_none(
            id=task_id, topic_id=topic_id, is_published=True
        )
        if task is None:
            raise TaskNotFoundException
        return validate_schema(task, TaskPublishedDto)

    async def mark_task_completion(
        self, topic_slug: str, task_id: int, data: TaskProgressPatchDto
    ) -> None:
        topic_id = await self._resolve_topic_id(topic_slug)
        task = await self.db.tasks.get_one_or_none(
            id=task_id, topic_id=topic_id, is_published=True
        )
        if task is None:
            raise TaskNotFoundException

        update_dto = TaskProgressUpdateDto(
            is_completed=data.is_completed,
            completed_at=datetime.now(timezone.utc) if data.is_completed else None,
        )

        try:
            await self.db.tasks.edit(id=task_id, data=update_dto, exclude_unset=False)
            await self.db.commit()
        except ObjectNotFoundException as ex:
            raise TaskNotFoundException from ex
