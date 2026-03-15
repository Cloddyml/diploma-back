from app.models import SubmissionsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import SubmissionDataMapper


class SubmissionsRepository(BaseRepository):
    model: SubmissionsOrm = SubmissionsOrm  # pyright: ignore[reportIncompatibleVariableOverride, reportAssignmentType]
    mapper = SubmissionDataMapper  # pyright: ignore[reportUnannotatedClassAttribute]
