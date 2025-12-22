from abc import abstractmethod
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.implementations.sqlalchemy_repository import (
    AlchSoftDeleteRepository,
)
from app.core.interfaces.base_repositories import (
    SoftDeleteRepository,
)

from .user_model import User
from .user_schemas import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)


class UserRepository(
    SoftDeleteRepository[
        User, UserCreateSchema, UserUpdateSchema, UserResponseSchema
    ],
    Protocol,
):
    @abstractmethod
    async def get_by_telegram_id(
        self, session: AsyncSession, telegram_id: str
    ) -> UserResponseSchema:
        """Получить пользователя по telegram_id"""


class AlchUserRepository(
    AlchSoftDeleteRepository[
        User, UserCreateSchema, UserUpdateSchema, UserResponseSchema
    ]
):
    def __init__(
        self,
        model: type[User],
        response_schema: type[UserResponseSchema],
    ):
        super().__init__(model, response_schema)

    async def get_by_telegram_id(
        self, session: AsyncSession, telegram_id: str
    ) -> UserResponseSchema | None:
        statement = select(self.model).where(
            self.model.telegram_id == telegram_id
        )
        statement = self._apply_disabled_filter(statement)
        result = await session.execute(statement)
        model_instance = result.scalar_one_or_none()
        return self._to_schema(model_instance)
