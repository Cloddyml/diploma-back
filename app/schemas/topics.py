import re
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints, field_validator


class TopicAddRequestDto(BaseModel):
    slug: Annotated[str, StringConstraints(max_length=100, to_lower=True)]
    title: str = Field(max_length=255)
    content: str | None = Field(None)
    order_index: int = Field(0, ge=0)
    is_published: bool = Field(False)

    @field_validator("slug", "title", mode="before")
    @classmethod
    def strip_whitespaces(cls, v: str) -> str:
        return v.strip()

    @field_validator("content", mode="before")
    @classmethod
    def strip_content(cls, v: str | None) -> str | None:
        if v is not None:
            return v.strip() or None
        return v

    @field_validator("slug", "title")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v:
            raise ValueError(
                "Поле не может быть пустым или состоять только из пробелов"
            )
        return v

    @field_validator("slug")
    @classmethod
    def normalize_slug(cls, v: str) -> str:
        return re.sub(r"\s+", "-", v).lower()


class TopicPutRequestDto(BaseModel):
    slug: Annotated[str, StringConstraints(max_length=100, to_lower=True)]
    title: str = Field(max_length=255)
    content: str
    order_index: int = Field(ge=0)
    is_published: bool

    @field_validator("slug", "title", mode="before")
    @classmethod
    def strip_whitespaces(cls, v: str) -> str:
        return v.strip()

    @field_validator("content", mode="before")
    @classmethod
    def strip_content(cls, v: str | None) -> str | None:
        if v is not None:
            return v.strip() or None
        return v

    @field_validator("slug", "title")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v:
            raise ValueError(
                "Поле не может быть пустым или состоять только из пробелов"
            )
        return v

    @field_validator("slug")
    @classmethod
    def normalize_slug(cls, v: str) -> str:
        return re.sub(r"\s+", "-", v).lower()


class TopicPatchRequestDto(BaseModel):
    slug: Annotated[str | None, StringConstraints(max_length=100, to_lower=True)] = None
    title: str | None = Field(None, max_length=255)
    content: str | None = Field(None)
    order_index: int | None = Field(None, ge=0)
    is_published: bool | None = Field(None)

    @field_validator("slug", "title", "content", mode="before")
    @classmethod
    def strip_whitespaces(cls, v: str | None) -> str | None:
        if v is not None:
            return v.strip() or None
        return v

    @field_validator("slug", "title")
    @classmethod
    def not_blank(cls, v: str | None) -> str | None:
        if v is not None and not v:
            raise ValueError(
                "Поле не может быть пустым или состоять только из пробелов"
            )
        return v

    @field_validator("slug")
    @classmethod
    def normalize_slug(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return re.sub(r"\s+", "-", v).lower()


class TopicDto(TopicAddRequestDto):
    id: int
    created_at: datetime


class TopicPublishedDto(BaseModel):
    slug: str
    title: str
    content: str | None = Field(None)
    order_index: int
