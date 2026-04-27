from datetime import date

from pydantic import BaseModel


class DailyStatDto(BaseModel):
    date: date
    submissions_total: int
    submissions_accepted: int
    tasks_completed: int


class ProgressResponseDto(BaseModel):
    total_topics: int
    completed_topics: int
    total_tasks: int
    completed_tasks: int
    daily_stats: list[DailyStatDto]
