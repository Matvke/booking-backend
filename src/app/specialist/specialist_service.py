from sqlalchemy.ext.asyncio import AsyncSession

from .specialist_repository import SpecialistRepository
from .specialist_schemas import (
    SpecialistCreateSchema,
    SpecialistResponseSchema,
    SpecialistUpdateSchema,
)


class SpecialistService:
    def __init__(self, specialist_repository: SpecialistRepository):
        self._specialist_repository: SpecialistRepository = specialist_repository

    @property
    def specialist_repository(self) -> SpecialistRepository:
        return self._specialist_repository

    async def create_specialist(
        self, session: AsyncSession, data: SpecialistCreateSchema
    ) -> SpecialistResponseSchema:
        return await self.specialist_repository.create(session, data)

    async def update_specialist(
        self, session: AsyncSession, specialist_id: int, schema: SpecialistUpdateSchema
    ) -> SpecialistResponseSchema:
        return await self.specialist_repository.update(session, specialist_id, schema)

    async def get_specialist_by_id(
        self, session: AsyncSession, specialist_id: int
    ) -> SpecialistResponseSchema:
        return await self.specialist_repository.get_by_id(session, specialist_id)

    async def create_invoke_token(
        self, session: AsyncSession, specialist_id: int
    ) -> str:
        return await self.specialist_repository.create_invoke_token(
            session, specialist_id
        )

    async def get_invoke_token(self, session: AsyncSession, specialist_id: int) -> str:
        return await self.specialist_repository.get_invoke_token(session, specialist_id)

    async def delete_invoke_token(
        self, session: AsyncSession, specialist_id: int
    ) -> str:
        return await self.specialist_repository.delete_invoke_token(
            session, specialist_id
        )

    async def verify_invoke_token(
        self, session: AsyncSession, specialist_id: int, invoke_token: str
    ) -> None:
        actual_token = await self.specialist_repository.get_invoke_token(
            session, specialist_id
        )
        if invoke_token == actual_token:
            return
        else:
            raise ValueError("Invalid invitation token")

    async def get_telegram_id(self, session: AsyncSession, specialist_id: int) -> str:
        return await self.specialist_repository.get_telegram_id(session, specialist_id)
