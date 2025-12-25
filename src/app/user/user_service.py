from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

from .user_exceptions import UserAlreadyExistsError, UserNotFoundError
from .user_repository import UserRepository
from .user_schemas import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)


class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository: UserRepository = user_repository

    @property
    def user_repository(self) -> UserRepository:
        return self._user_repository

    async def create_user(
        self, session: AsyncSession, data: UserCreateSchema
    ) -> UserResponseSchema:
        try:
            user = await self.user_repository.create(session, data)
        except IntegrityError as e:
            if settings.DEBUG:
                raise UserAlreadyExistsError(str(e))
            else:
                raise UserAlreadyExistsError()
        return user

    async def update_user(
        self, session: AsyncSession, user_id: int, schema: UserUpdateSchema
    ) -> UserResponseSchema:
        return await self.user_repository.update(session, user_id, schema)

    async def get_user_by_id(
        self, session: AsyncSession, user_id: int
    ) -> UserResponseSchema:
        user = await self.user_repository.get_by_id(session, user_id)
        if user is None:
            raise UserNotFoundError(
                key="User ID",
                value=user_id,
            )
        return user

    async def get_user_by_telegram_id(
        self, session: AsyncSession, telegram_id: str
    ) -> UserResponseSchema:
        user = await self.user_repository.get_by_telegram_id(session, telegram_id)
        if user is None:
            raise UserNotFoundError(
                key="Telegram ID",
                value=telegram_id,
            )
        return user
