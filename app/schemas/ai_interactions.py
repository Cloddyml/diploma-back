from datetime import datetime

from pydantic import BaseModel, Field


class AIInteractionDto(BaseModel):
    id: int
    task_id: int | None = Field(None)
    topic_id: int | None = Field(None)
    user_message: str | None = Field(None)
    ai_response: str | None = Field(None)
    created_at: datetime
