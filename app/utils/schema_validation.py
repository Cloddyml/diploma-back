from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def validate_schema(data: BaseModel, schema_to: type[T]) -> T:
    """Преобразует одну Pydantic-схему в другую за один проход по атрибутам."""
    return schema_to.model_validate(data, from_attributes=True)
