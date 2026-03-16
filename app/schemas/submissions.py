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
    created_at: datetime


class SubmissionSubmitRequestDto(BaseModel):
    """Входящие данные от пользователя при предоставлении кода"""

    code: str


class SubmissionAddDto(SubmissionSubmitRequestDto):
    """Внутренняя DTO для вставки в БД"""

    task_id: int


class SubmissionCreatedDto(BaseModel):
    """
    Клиент получает ID и идёт поллить GET
    после получения ответа об успешном предоставлении кода
    """

    submission_id: int
