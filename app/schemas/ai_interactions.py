from datetime import datetime

from pydantic import BaseModel, Field


class AIInteractionAddDto(BaseModel):
    task_id: int | None = Field(None)
    topic_id: int | None = Field(None)
    user_message: str | None = Field(None)
    ai_response: str | None = Field(None)


class AIInteractionDto(AIInteractionAddDto):
    id: int
    created_at: datetime


class AIInteractionTaskHintRequestDto(BaseModel):
    task_id: int
    user_message: str


class AIInteractionTopicHintRequestDto(BaseModel):
    topic_id: int
    user_message: str


class AIInteractionHintResponseDto(BaseModel):
    ai_response: str
