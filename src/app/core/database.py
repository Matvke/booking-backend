from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


DATABASE_URL = settings.get_db_url()

engine = create_async_engine(
    DATABASE_URL,
    pool_size=30,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)

async_session_factory = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession, autobegin=False
)


class Base(DeclarativeBase):
    pass
