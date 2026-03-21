from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class TaskAddRequestDto(BaseModel):
    title: str = Field(max_length=255)
    description: str
    starter_code: str | None = Field(None)
    solution_code: str | None = Field(None)
    order_index: int = Field(0, ge=0)
    time_limit_sec: int = Field(10)
    memory_limit_mb: int = Field(128)
    is_published: bool = Field(False)
    topic_id: int | None = Field(None)

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_whitespaces(cls, v: str) -> str:
        return v.strip()

    @field_validator("title", "description")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v:
            raise ValueError(
                "Поле не может быть пустым или состоять только из пробелов"
            )
        return v


class TaskPutRequestDto(BaseModel):
    title: str = Field(max_length=255)
    description: str
    starter_code: str | None = None
    solution_code: str | None = None
    order_index: int = Field(ge=0)
    time_limit_sec: int
    memory_limit_mb: int
    is_published: bool
    topic_id: int | None = Field(None)

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_whitespaces(cls, v: str) -> str:
        return v.strip()

    @field_validator("title", "description")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v:
            raise ValueError(
                "Поле не может быть пустым или состоять только из пробелов"
            )
        return v


class TaskPatchRequestDto(BaseModel):
    title: str | None = Field(None, max_length=255)
    description: str | None = None
    starter_code: str | None = None
    order_index: int | None = Field(None, ge=0)
    time_limit_sec: int | None = None
    memory_limit_mb: int | None = None
    is_published: bool | None = None
    topic_id: int | None = Field(None)

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_whitespaces(cls, v: str | None) -> str | None:
        if v is not None:
            return v.strip() or None
        return v

    @field_validator("title", "description")
    @classmethod
    def not_blank(cls, v: str | None) -> str | None:
        if v is not None and not v:
            raise ValueError(
                "Поле не может быть пустым или состоять только из пробелов"
            )
        return v


class TaskDto(BaseModel):
    id: int
    topic_id: int
    title: str = Field(max_length=255)
    description: str
    starter_code: str | None = Field(None)
    solution_code: str | None = Field(None)
    order_index: int = Field(0)
    time_limit_sec: int = Field(10)
    memory_limit_mb: int = Field(128)
    is_published: bool = Field(False)
    is_completed: bool = Field(False)
    created_at: datetime


class TaskPublishedDto(BaseModel):
    id: int
    title: str = Field(max_length=255)
    description: str
    starter_code: str | None = Field(None)
    order_index: int = Field(0)
    time_limit_sec: int = Field(10)
    memory_limit_mb: int = Field(128)
    is_completed: bool


class TaskProgressPatchDto(BaseModel):
    is_completed: bool
