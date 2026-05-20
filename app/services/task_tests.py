from app.exceptions.excs import TaskNotFoundException, TopicNotFoundException
from app.schemas import TaskTestDto
from app.services.base import BaseService


class TaskTestsService(BaseService):
    async def _resolve_topic_id(self, topic_slug: str) -> int:
        topic = await self.db.topics.get_one_or_none(
            slug=topic_slug, is_published=True
        )
        if topic is None:
            raise TopicNotFoundException
        return topic.id

    async def _resolve_task_id(self, topic_slug: str, task_id: int) -> int:
        topic_id = await self._resolve_topic_id(topic_slug)
        task = await self.db.tasks.get_one_or_none(
            id=task_id, topic_id=topic_id, is_published=True
        )
        if task is None:
            raise TaskNotFoundException
        return task.id

    async def get_visible_tests_by_task(
        self, topic_slug: str, task_id: int
    ) -> list[TaskTestDto]:
        await self._resolve_task_id(topic_slug, task_id)
        return await self.db.task_tests.get_visible_tests_by_task_id(task_id=task_id)
