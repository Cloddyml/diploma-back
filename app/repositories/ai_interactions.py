from app.models import AIInteractionsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import AIInteractionDataMapper


class AIInteractionsRepository(BaseRepository):
    model: AIInteractionsOrm = AIInteractionsOrm  # pyright: ignore[reportIncompatibleVariableOverride, reportAssignmentType]
    mapper = AIInteractionDataMapper  # pyright: ignore[reportUnannotatedClassAttribute]
