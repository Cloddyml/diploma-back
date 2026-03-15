from datetime import datetime

from pydantic import BaseModel, Field


class TaskDto(BaseModel):
    id: int
    topic_id: int
    title: str = Field(max_length=255)
    description: str
    starter_code: str | None
    solution_code: str | None
    order_index: int = Field(0)
    time_limit_sec: int = Field(10)
    memory_limit_mb: int = Field(128)
    is_published: bool = Field(False)
    created_at: datetime
