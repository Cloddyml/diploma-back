from datetime import datetime

from pydantic import BaseModel, Field


class TaskAddRequestDto(BaseModel):
    topic_id: int
    title: str = Field(max_length=255)
    description: str
    starter_code: str | None = Field(None)
    order_index: int = Field(0)
    time_limit_sec: int = Field(10)
    memory_limit_mb: int = Field(128)
    is_published: bool = Field(False)


class TaskDto(TaskAddRequestDto):
    id: int
    solution_code: str | None = Field(None)
    created_at: datetime


class TaskPublishedDto(BaseModel):
    title: str = Field(max_length=255)
    description: str
    order_index: int = Field(0)
