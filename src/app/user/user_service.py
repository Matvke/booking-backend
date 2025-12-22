from .user_repository import UserRepository
from .user_schemas import (
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
)
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository: UserRepository = user_repository

    @property
    def user_repository(self) -> UserRepository:
        return self._user_repository

    async def create_user(
        self, session: AsyncSession, data: UserCreateSchema
    ) -> UserResponseSchema:
        return await self.user_repository.create(session, data)

    async def update_user(
        self, session: AsyncSession, id: int, schema: UserUpdateSchema
    ) -> UserResponseSchema:
        return await self.user_repository.update(session, id, schema)

    async def get_user_by_id(
        self, session: AsyncSession, id: int
    ) -> UserResponseSchema:
        return await self.user_repository.get_by_id(session, id)

    async def get_user_by_telegram_id(
        self, session: AsyncSession, telegram_id: str
    ) -> UserResponseSchema:
        return await self.user_repository.get_by_telegram_id(session, telegram_id)
