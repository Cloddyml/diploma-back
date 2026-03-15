from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class TopicAddRequestDto(BaseModel):
    slug: Annotated[str, StringConstraints(max_length=100, to_lower=True)]
    title: str = Field(max_length=255)
    content: str | None = Field(None)
    order_index: int = Field(0)
    is_published: bool = Field(False)


class TopicDto(TopicAddRequestDto):
    id: int
    created_at: datetime


class TopicPublishedDto(BaseModel):
    slug: str
    title: str
    content: str | None = Field(None)
    order_index: int
