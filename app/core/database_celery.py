from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

sync_engine = create_engine(
    settings.SYNC_DB_URL,
    pool_pre_ping=True,
    pool_size=5,
)

sync_session_factory = sessionmaker(bind=sync_engine, expire_on_commit=False)
