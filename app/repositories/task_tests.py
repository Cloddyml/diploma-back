from sqlalchemy import select

from app.models import TaskTestsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import TaskTestDataMapper


class TaskTestsRepository(BaseRepository):
    model: TaskTestsOrm = TaskTestsOrm  # pyright: ignore[reportIncompatibleVariableOverride, reportAssignmentType]
    mapper = TaskTestDataMapper  # pyright: ignore[reportUnannotatedClassAttribute]

    async def get_tests_by_task_id(self, task_id: int):
        query = select(TaskTestsOrm).where(TaskTestsOrm.task_id == task_id)
        result = await self.session.execute(query)
        tests = result.scalars().all()
        return [self.mapper.map_to_domain_entity(test) for test in tests]

    async def get_visible_tests_by_task_id(self, task_id: int):
        query = select(TaskTestsOrm).where(
            TaskTestsOrm.task_id == task_id,
            TaskTestsOrm.is_hidden.is_(False),
        )
        result = await self.session.execute(query)
        tests = result.scalars().all()
        return [self.mapper.map_to_domain_entity(test) for test in tests]
