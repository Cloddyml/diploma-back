from typing import Any

from asyncpg.exceptions import NotNullViolationError, UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import delete as sa_delete
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base
from app.exceptions.excs import (
    CannotBeEmptyException,
    EmptyUpdateDataException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
)
from app.repositories.mappers.base import DataMapper


class RepositoryBase:
    """Общий родитель для всех репозиториев. Хранит ссылку на сессию."""

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session


class BaseRepository(RepositoryBase):
    model: type[Base]  # pyright: ignore[reportUninitializedInstanceVariable]  # noqa: UP006
    mapper: type[DataMapper]  # pyright: ignore[reportUninitializedInstanceVariable]  # noqa: UP006

    async def get_filtered(self, *filters, **filter_by) -> list[BaseModel | Any]:
        query = select(self.model).filter(*filters).filter_by(**filter_by)
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

    async def add(self, data: BaseModel) -> int:
        add_data_stmt = (
            insert(self.model)
            .values(**self.mapper.map_to_persistence_entity(data))
            .returning(self.model.id)
        )
        try:
            result = await self.session.execute(add_data_stmt)
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            else:
                raise ex
        return result.scalar_one()

    async def edit(
        self,
        data: BaseModel,
        exclude_unset: bool = False,
        exclude_none: bool = False,
        **filter_by,
    ) -> None:
        obj = await self.get_one_or_none(**filter_by)
        if obj is None:
            raise ObjectNotFoundException
        values = self.mapper.map_to_persistence_entity(
            data=data, exclude_unset=exclude_unset, exclude_none=exclude_none
        )
        if not values:
            raise EmptyUpdateDataException

        update_stmt = update(self.model).filter_by(**filter_by).values(**values)
        try:
            await self.session.execute(update_stmt)
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, NotNullViolationError):
                raise CannotBeEmptyException from ex
            else:
                raise ex

    async def delete(self, **filter_by) -> None:
        obj = await self.get_one_or_none(**filter_by)
        if obj is None:
            raise ObjectNotFoundException
        delete_stmt = sa_delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
