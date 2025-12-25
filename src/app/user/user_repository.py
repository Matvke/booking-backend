from abc import abstractmethod
from typing import Protocol

from sqlalchemy import Insert, Update, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import UserRole
from app.core.implementations.sqlalchemy_repository import (
    AlchSoftDeleteRepository,
)
from app.core.interfaces.base_repositories import (
    SoftDeleteRepository,
)
from app.specialist.specialist_model import Specialist

from .user_model import User
from .user_schemas import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)


class UserRepository(
    SoftDeleteRepository[User, UserCreateSchema, UserUpdateSchema, UserResponseSchema],
    Protocol,
):
    @abstractmethod
    async def get_by_telegram_id(
        self, session: AsyncSession, telegram_id: str
    ) -> UserResponseSchema | None:
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

    async def _get_role(self, session: AsyncSession, user_id: int) -> UserRole:
        """Определить роль пользователя"""
        statement = select(Specialist).where(Specialist.user_id == user_id)
        result = await session.execute(statement)
        specialist = result.scalar_one_or_none()
        role = UserRole.USER
        if specialist:
            role = UserRole.SPECIALIST
            if specialist.is_admin:
                role = UserRole.ADMIN
        return role

    async def create(
        self, session: AsyncSession, data: UserCreateSchema
    ) -> UserResponseSchema:
        entity_data = data.model_dump()
        statement: Insert = (
            insert(self.model).values(**entity_data).returning(self.model)
        )
        result = await session.execute(statement)
        await session.flush()
        model_instance = result.scalar_one()
        role = await self._get_role(session, model_instance.id)
        return self._to_schema_with_role(model_instance, role)

    async def update(
        self, session: AsyncSession, id: int, data: UserUpdateSchema
    ) -> UserCreateSchema:
        values = data.model_dump(exclude_unset=True)

        statement: Update = (
            update(self.model)
            .where(self.model.id == id)
            .values(**values)
            .returning(self.model)
        )
        statement = self._apply_disabled_filter(statement)
        result = await session.execute(statement)
        await session.flush()
        model_instance = result.scalar_one()
        role = await self._get_role(session, id)
        return self._to_schema_with_role(model_instance, role)

    async def get_by_telegram_id(
        self, session: AsyncSession, telegram_id: str
    ) -> UserResponseSchema | None:
        statement = select(self.model).where(self.model.telegram_id == telegram_id)
        statement = self._apply_disabled_filter(statement)
        result = await session.execute(statement)
        model_instance = result.scalar_one_or_none()
        if model_instance is None:
            return None
        role = await self._get_role(session, model_instance.id)
        return self._to_schema_with_role(model_instance, role)

    def _to_schema_with_role(
        self, model_instance: User | None, role: UserRole
    ) -> UserResponseSchema | None:
        """Преобразовать модель в схему с указанной ролью"""
        if model_instance is None:
            return None

        model_dict = {}
        for column in model_instance.__table__.columns:
            model_dict[column.name] = getattr(model_instance, column.name)

        model_dict["role"] = role

        return self.response_schema.model_validate(model_dict)
