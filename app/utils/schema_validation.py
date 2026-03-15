from pydantic import BaseModel


def validate_schema(data: BaseModel, schema_to: BaseModel) -> BaseModel:
    return schema_to.model_validate(data.model_dump())
