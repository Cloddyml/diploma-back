from app.models import (
    AIInteractionsOrm,
    SubmissionsOrm,
    TasksOrm,
    TaskTestsOrm,
    TopicsOrm,
)
from app.repositories.mappers.base import DataMapper
from app.schemas.ai_interactions import AIInteractionDto
from app.schemas.submissions import SubmissionDto
from app.schemas.task_tests import TaskTestDto
from app.schemas.tasks import TaskDto
from app.schemas.topics import TopicDto


class AIInteractionDataMapper(DataMapper):
    db_model = AIInteractionsOrm  # pyright: ignore[reportUnannotatedClassAttribute]
    schema = AIInteractionDto  # pyright: ignore[reportUnannotatedClassAttribute]


class SubmissionDataMapper(DataMapper):
    db_model = SubmissionsOrm  # pyright: ignore[reportUnannotatedClassAttribute]
    schema = SubmissionDto  # pyright: ignore[reportUnannotatedClassAttribute]


class TaskTestDataMapper(DataMapper):
    db_model = TaskTestsOrm  # pyright: ignore[reportUnannotatedClassAttribute]
    schema = TaskTestDto  # pyright: ignore[reportUnannotatedClassAttribute]


class TaskDataMapper(DataMapper):
    db_model = TasksOrm  # pyright: ignore[reportUnannotatedClassAttribute]
    schema = TaskDto  # pyright: ignore[reportUnannotatedClassAttribute]


class TopicDataMapper(DataMapper):
    db_model = TopicsOrm  # pyright: ignore[reportUnannotatedClassAttribute]
    schema = TopicDto  # pyright: ignore[reportUnannotatedClassAttribute]
