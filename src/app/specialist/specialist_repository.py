import random
import string
from abc import abstractmethod
from typing import Protocol

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.implementations.sqlalchemy_repository import (
    AlchSoftDeleteRepository,
)
from app.core.interfaces.base_repositories import (
    SoftDeleteRepository,
)
from app.user.user_model import User
from app.user.user_schemas import UserResponseSchema

from .specialist_model import Specialist
from .specialist_schemas import (
    SpecialistCreateSchema,
    SpecialistResponseSchema,
    SpecialistUpdateSchema,
)


class SpecialistRepository(
    SoftDeleteRepository[
        Specialist,
        SpecialistCreateSchema,
        SpecialistUpdateSchema,
        SpecialistResponseSchema,
    ],
    Protocol,
):
    @abstractmethod
    async def create_invoke_token(
        self, session: AsyncSession, specialist_id: int
    ) -> str:
        """Сгенерировать новый код приглашения для специалиста.
        Возвращает invite token."""

    @abstractmethod
    async def get_invoke_token(self, session: AsyncSession, specialist_id: int) -> str:
        """Получить имеющийся код приглашения для специалиста.
        Возвращает invite token."""

    @abstractmethod
    async def delete_invoke_token(
        self, session: AsyncSession, specialist_id: int
    ) -> None:
        """Удалить имеющийся код приглашения для специалиста."""

    @abstractmethod
    async def get_telegram_id(
        self, session: AsyncSession, specialist_id: int
    ) -> UserResponseSchema:
        """Вернуть телеграм пользователя, к которому привязан аккаунт специалиста."""


class AlchSpecialistRepository(
    AlchSoftDeleteRepository[
        Specialist,
        SpecialistCreateSchema,
        SpecialistUpdateSchema,
        SpecialistResponseSchema,
    ]
):
    def __init__(
        self,
        model: type[Specialist],
        response_schema: type[SpecialistResponseSchema],
    ):
        super().__init__(model, response_schema)

    async def create_invoke_token(
        self, session: AsyncSession, specialist_id: int
    ) -> str:
        statement = (
            update(self.model)
            .where(self.model.id == specialist_id)
            .values({self.model.invoke_token: self._generate_invoke_token()})
            .returning(self.model.invoke_token)
        )
        statement = self._apply_disabled_filter(statement)
        result = await session.execute(statement)
        await session.flush()
        return result.scalar_one()

    async def get_invoke_token(self, session: AsyncSession, specialist_id: int) -> str:
        statement = select(self.model.invoke_token).where(
            self.model.id == specialist_id
        )
        statement = self._apply_disabled_filter(statement)
        result = await session.execute(statement)
        await session.flush()
        return result.scalar_one()

    async def delete_invoke_token(
        self, session: AsyncSession, specialist_id: int
    ) -> None:
        statement = (
            update(self.model)
            .where(self.model.id == specialist_id)
            .values({self.model.invoke_token: None})
            .returning(self.model.invoke_token)
        )
        statement = self._apply_disabled_filter(statement)
        result = await session.execute(statement)
        await session.flush()
        return result.scalar_one()

    def _generate_invoke_token(self, invoke_token_len: int = 4) -> str:
        return "".join(
            random.choice(string.ascii_lowercase) for _ in range(invoke_token_len)
        )

    async def get_telegram_id(self, session: AsyncSession, specialist_id: int) -> str:
        statement = (
            select(User.telegram_id)
            .select_from(self.model)
            .join(User, self.model.user_id == User.id)
            .where(self.model.id == specialist_id)
        )
        statement = self._apply_disabled_filter(statement)
        result = await session.execute(statement)
        return result.scalar_one_or_none()
