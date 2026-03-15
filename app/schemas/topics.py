from datetime import datetime

from pydantic import BaseModel, Field


class TopicAddRequestDto(BaseModel):
    slug: str = Field(max_length=100)
    title: str = Field(max_length=255)
    content: str | None = Field(None)
    order_index: int = Field(0)
    is_published: bool = Field(False)


class TopicDto(TopicAddRequestDto):
    id: int
    created_at: datetime
