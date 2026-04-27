from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def validate_schema(data: BaseModel, schema_to: type[T]) -> T:
    return schema_to.model_validate(data.model_dump())
