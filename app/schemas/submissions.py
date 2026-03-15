from datetime import datetime

from pydantic import BaseModel, Field

from app.models.submissions import SubmissionStatus


class SubmissionDto(BaseModel):
    id: int
    task_id: int
    code: str
    status: SubmissionStatus
    result: str | None = Field(None)
    error: str | None = Field(None)
    created_at: datetime = Field(datetime.now())
