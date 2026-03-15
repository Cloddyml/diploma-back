from app.exceptions.excs import TaskNotFoundException
from app.models import TasksOrm
from app.schemas import TaskPublishedDto
from app.services.base import BaseService
from app.utils.schema_validation import validate_schema


class TasksService(BaseService):
    async def get_all_published_tasks_by_topic(
        self, slug: str
    ) -> list[TaskPublishedDto]:
        tasks = await self.db.tasks.get_published_tasks_by_topic_slug(slug=slug)
        if not tasks:
            raise TaskNotFoundException
        return [validate_schema(task, TaskPublishedDto) for task in tasks]
