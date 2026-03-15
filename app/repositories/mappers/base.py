from typing import Any, TypeVar

from pydantic import BaseModel

from app.core.database import Base

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: type[Base]  # pyright: ignore[reportUninitializedInstanceVariable]
    schema: type[SchemaType]  # type: ignore  # pyright: ignore[reportUninitializedInstanceVariable, reportGeneralTypeIssues]

    @classmethod
    def map_to_domain_entity(cls, data: Base) -> BaseModel:
        """ORM-модель → Pydantic-схема"""
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: BaseModel) -> dict[Any, Any]:  # pyright: ignore[reportExplicitAny]
        """Pydantic-схема → dict для INSERT/UPDATE"""
        return data.model_dump()
