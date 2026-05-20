from sqlalchemy.sql import select

from app.models import TasksOrm
from app.models.topics import TopicsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import TaskDataMapper


class TasksRepository(BaseRepository):
    model: TasksOrm = TasksOrm  # pyright: ignore[reportIncompatibleVariableOverride, reportAssignmentType]
    mapper = TaskDataMapper  # pyright: ignore[reportUnannotatedClassAttribute]

    async def get_published_tasks_by_topic_slug(self, slug: str):
        query = (
            select(TasksOrm)
            .join(TopicsOrm, TopicsOrm.id == TasksOrm.topic_id)
            .where(TopicsOrm.slug == slug, TasksOrm.is_published)
        )
        result = await self.session.execute(query)
        tasks = result.scalars().all()
        return [self.mapper.map_to_domain_entity(task) for task in tasks]
