from typing import Any

from pydantic import BaseModel
from sqlalchemy import delete as sa_delete
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base
from app.repositories.mappers.base import DataMapper


class BaseRepository:
    model: type[Base]  # pyright: ignore[reportUninitializedInstanceVariable]  # noqa: UP006
    mapper: type[DataMapper]  # pyright: ignore[reportUninitializedInstanceVariable]  # noqa: UP006
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(self, *filter, **filter_by) -> list[BaseModel | Any]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_all(self) -> list[BaseModel | Any]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by) -> BaseModel | None | Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        model = result.scalars().one()

        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel) -> BaseModel | Any:
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def edit(
        self, data: BaseModel, exclude_unset: bool = False, **filter_by
    ) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = sa_delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
