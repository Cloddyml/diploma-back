from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class DBManager:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory: async_sessionmaker[AsyncSession] = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()  # pyright: ignore

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
