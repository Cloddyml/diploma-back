from app.models import TasksOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import TaskDataMapper


class TasksRepository(BaseRepository):
    model: TasksOrm = TasksOrm  # pyright: ignore[reportIncompatibleVariableOverride, reportAssignmentType]
    mapper = TaskDataMapper  # pyright: ignore[reportUnannotatedClassAttribute]
