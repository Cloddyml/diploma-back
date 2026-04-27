from app.models import TasksOrm, TopicsOrm
from app.schemas.progress import ProgressResponseDto
from app.services.base import BaseService


class ProgressService(BaseService):
    async def get_progress(self, days: int = 30) -> ProgressResponseDto:
        all_topics = await self.db.topics.get_filtered(TopicsOrm.is_published)
        completed_topics = [t for t in all_topics if t.is_completed]

        all_tasks = await self.db.tasks.get_filtered(TasksOrm.is_published)
        completed_tasks = [t for t in all_tasks if t.is_completed]

        daily_stats = await self.db.progress.get_daily_stats(days=days)

        return ProgressResponseDto(
            total_topics=len(all_topics),
            completed_topics=len(completed_topics),
            total_tasks=len(all_tasks),
            completed_tasks=len(completed_tasks),
            daily_stats=daily_stats,
        )
