from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.repositories import (
    AIInteractionsRepository,
    ProgressRepository,
    SubmissionsRepository,
    TasksRepository,
    TaskTestsRepository,
    TopicsRepository,
)


class DBManager:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory: async_sessionmaker[AsyncSession] = session_factory

    def _setup_repositories(self, session: AsyncSession) -> None:
        self.session = session
        self.ai_interactions = AIInteractionsRepository(session)
        self.submissions = SubmissionsRepository(session)
        self.tasks = TasksRepository(session)
        self.task_tests = TaskTestsRepository(session)
        self.topics = TopicsRepository(session)
        self.progress = ProgressRepository(session)

    @classmethod
    def from_session(cls, session: AsyncSession) -> "DBManager":
        instance = cls.__new__(cls)
        instance._setup_repositories(session)
        return instance

    async def __aenter__(self):
        self._setup_repositories(self.session_factory())
        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
