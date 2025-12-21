from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_factory
from app.core.implementations.uow import UnitOfWork


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    uow = UnitOfWork(async_session_factory)
    async with uow as session:
        yield session
