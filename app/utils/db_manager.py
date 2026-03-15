from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.repositories import (
    AIInteractionsRepository,
    SubmissionsRepository,
    TasksRepository,
    TaskTestsRepository,
    TopicsRepository,
)


class DBManager:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory: async_sessionmaker[AsyncSession] = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()  # pyright: ignore[reportUnannotatedClassAttribute, reportUninitializedInstanceVariable]

        self.ai_interactions = AIInteractionsRepository(self.session)  # pyright: ignore[reportUnannotatedClassAttribute, reportUninitializedInstanceVariable]
        self.submissions = SubmissionsRepository(self.session)  # pyright: ignore[reportUnannotatedClassAttribute, reportUninitializedInstanceVariable]
        self.tasks = TasksRepository(self.session)  # pyright: ignore[reportUnannotatedClassAttribute, reportUninitializedInstanceVariable]
        self.task_tests = TaskTestsRepository(self.session)  # pyright: ignore[reportUnannotatedClassAttribute, reportUninitializedInstanceVariable]
        self.topics = TopicsRepository(self.session)  # pyright: ignore[reportUnannotatedClassAttribute, reportUninitializedInstanceVariable]

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
