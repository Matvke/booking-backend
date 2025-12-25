from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

from .specialist_exceptions import (
    SpecialistAlreadyExistsError,
    SpecialistHasNoTelegramError,
    SpecialistNotFoundError,
    SpecialistVerificationError,
)
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
        try:
            return await self.specialist_repository.create(session, data)
        except IntegrityError as e:
            if settings.DEBUG:
                raise SpecialistAlreadyExistsError(str(e))
            else:
                raise SpecialistAlreadyExistsError()

    async def update_specialist(
        self, session: AsyncSession, specialist_id: int, schema: SpecialistUpdateSchema
    ) -> SpecialistResponseSchema:
        return await self.specialist_repository.update(session, specialist_id, schema)

    async def get_specialist_by_id(
        self, session: AsyncSession, specialist_id: int
    ) -> SpecialistResponseSchema:
        specialist = await self.specialist_repository.get_by_id(session, specialist_id)
        if specialist is None:
            raise SpecialistNotFoundError(key="Specialist ID", value=specialist_id)
        return specialist

    async def create_invoke_token(
        self, session: AsyncSession, specialist_id: int
    ) -> str:
        token = await self.specialist_repository.create_invoke_token(
            session, specialist_id
        )
        if token is None:
            raise SpecialistNotFoundError(key="Specialist ID", value=specialist_id)

    async def get_invoke_token(self, session: AsyncSession, specialist_id: int) -> str:
        token = await self.specialist_repository.get_invoke_token(
            session, specialist_id
        )
        if token is None:
            raise SpecialistNotFoundError(key="Specialist ID", value=specialist_id)

    async def delete_invoke_token(
        self, session: AsyncSession, specialist_id: int
    ) -> None:
        try:
            return await self.specialist_repository.delete_invoke_token(
                session, specialist_id
            )
        except NoResultFound:
            raise SpecialistNotFoundError(key="Specialist ID", value=specialist_id)

    async def verify_invoke_token(
        self, session: AsyncSession, specialist_id: int, invoke_token: str
    ) -> None:
        actual_token = await self.specialist_repository.get_invoke_token(
            session, specialist_id
        )
        if invoke_token == actual_token:
            return
        else:
            raise SpecialistVerificationError()

    async def get_telegram_id(self, session: AsyncSession, specialist_id: int) -> str:
        telegram_id = await self.specialist_repository.get_telegram_id(
            session, specialist_id
        )
        if telegram_id is None:
            raise SpecialistHasNoTelegramError()
        return telegram_id
