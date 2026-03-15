from app.models import TaskTestsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import TaskTestDataMapper


class TaskTestsRepository(BaseRepository):
    model: TaskTestsOrm = TaskTestsOrm  # pyright: ignore[reportIncompatibleVariableOverride, reportAssignmentType]
    mapper = TaskTestDataMapper  # pyright: ignore[reportUnannotatedClassAttribute]
