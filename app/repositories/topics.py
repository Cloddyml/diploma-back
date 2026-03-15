from app.models import TopicsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import TopicDataMapper


class TopicsRepository(BaseRepository):
    model: TopicsOrm = TopicsOrm  # pyright: ignore[reportIncompatibleVariableOverride, reportAssignmentType]
    mapper = TopicDataMapper  # pyright: ignore[reportUnannotatedClassAttribute]
