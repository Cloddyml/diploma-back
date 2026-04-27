from datetime import date, datetime, timedelta, timezone

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.submissions import SubmissionsOrm, SubmissionStatus
from app.models.tasks import TasksOrm
from app.schemas.progress import DailyStatDto


class ProgressRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_daily_stats(self, days: int = 30) -> list[DailyStatDto]:
        since = datetime.now(timezone.utc) - timedelta(days=days)

        submissions_query = (
            select(
                func.date(SubmissionsOrm.created_at).label("day"),
                func.count().label("total"),
                func.sum(
                    case(
                        (SubmissionsOrm.status == SubmissionStatus.ACCEPTED, 1),
                        else_=0,
                    )
                ).label("accepted"),
            )
            .where(SubmissionsOrm.created_at >= since)
            .group_by(func.date(SubmissionsOrm.created_at))
        )

        submissions_result = await self.session.execute(submissions_query)
        submissions_by_day: dict[date, tuple[int, int]] = {
            row.day: (int(row.total), int(row.accepted or 0))
            for row in submissions_result
        }

        tasks_query = (
            select(
                func.date(TasksOrm.completed_at).label("day"),
                func.count().label("count"),
            )
            .where(
                TasksOrm.completed_at >= since,
                TasksOrm.is_completed.is_(True),
            )
            .group_by(func.date(TasksOrm.completed_at))
        )

        tasks_result = await self.session.execute(tasks_query)
        tasks_by_day: dict[date, int] = {
            row.day: int(row.count) for row in tasks_result
        }

        all_days: set[date] = set(submissions_by_day.keys()) | set(tasks_by_day.keys())

        return [
            DailyStatDto(
                date=day,
                submissions_total=submissions_by_day.get(day, (0, 0))[0],
                submissions_accepted=submissions_by_day.get(day, (0, 0))[1],
                tasks_completed=tasks_by_day.get(day, 0),
            )
            for day in sorted(all_days)
        ]
