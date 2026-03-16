from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.database import get_db
from app.core.config import settings
from app.core.database import Base
from app.core.database_test import async_session_maker_null_pool, engine_null_pool
from app.main import app
from app.repositories import (
    AIInteractionsRepository,
    SubmissionsRepository,
    TasksRepository,
    TaskTestsRepository,
    TopicsRepository,
)
from app.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def db(setup_database) -> AsyncGenerator[DBManager, None]:
    async with engine_null_pool.connect() as conn:
        await conn.begin()

        session = AsyncSession(
            bind=conn,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )

        db_manager = DBManager.__new__(DBManager)
        db_manager.session_factory = async_session_maker_null_pool
        db_manager.session = session
        db_manager.ai_interactions = AIInteractionsRepository(session)
        db_manager.submissions = SubmissionsRepository(session)
        db_manager.tasks = TasksRepository(session)
        db_manager.task_tests = TaskTestsRepository(session)
        db_manager.topics = TopicsRepository(session)

        try:
            yield db_manager
        finally:
            await session.close()
            await conn.rollback()


@pytest.fixture(scope="function")
async def client(db: DBManager):

    async def get_db_override():
        yield db

    app.dependency_overrides[get_db] = get_db_override
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.pop(get_db, None)
