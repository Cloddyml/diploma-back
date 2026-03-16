from pydantic import BaseModel
from sqlalchemy import insert

from app.models import SubmissionsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import SubmissionDataMapper


class SubmissionsRepository(BaseRepository):
    model: SubmissionsOrm = SubmissionsOrm  # pyright: ignore[reportIncompatibleVariableOverride, reportAssignmentType]
    mapper = SubmissionDataMapper  # pyright: ignore[reportUnannotatedClassAttribute]

    async def add_and_return_id(self, data: BaseModel) -> int:
        """
        Создаёт submission и возвращает его ID.
        """
        stmt = (
            insert(self.model)
            .values(**self.mapper.map_to_persistence_entity(data))
            .returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()
