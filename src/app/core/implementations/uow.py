from typing import Self
from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    def __init__(self, async_session_factory):
        self.session_factory = async_session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> Self:
        self.session = self.session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
