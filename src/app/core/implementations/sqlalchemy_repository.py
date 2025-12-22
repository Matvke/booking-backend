from typing import Any, Generic

from sqlalchemy import (
    Delete,
    Insert,
    Select,
    Update,
    delete,
    insert,
    not_,
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession

from ..interfaces.base_repositories import (
    CreateSchemaT,
    ModelT,
    ResponseSchemaT,
    SoftDeleteModelT,
    UpdateSchemaT,
)


class AlchRepository(Generic[ModelT, CreateSchemaT, UpdateSchemaT, ResponseSchemaT]):
    def __init__(
        self,
        model: type[ModelT],
        response_schema: type[ResponseSchemaT],
    ):
        self._model = model
        self._response_schema = response_schema
        if "disabled" in model.__dict__:
            raise TypeError(
                f"Model {model.__tablename__} has 'disabled' field. "
                f"Use AlchSoftDeleteRepository instead."
            )

    @property
    def model(self) -> type[ModelT]:
        return self._model

    @property
    def response_schema(self) -> type[ResponseSchemaT]:
        return self._response_schema

    def _to_schema(self, model_instance: ModelT | None) -> ResponseSchemaT | None:
        if model_instance is None:
            return None
        return self.response_schema.model_validate(model_instance)

    async def create(
        self, session: AsyncSession, data: CreateSchemaT
    ) -> ResponseSchemaT:
        entity_data = data.model_dump()
        statement: Insert = (
            insert(self.model).values(**entity_data).returning(self.model)
        )
        result = await session.execute(statement)
        await session.flush()
        model_instance = result.scalar_one()
        return self._to_schema(model_instance)

    async def update(
        self, session: AsyncSession, id: int, data: UpdateSchemaT
    ) -> ResponseSchemaT:
        values = data.model_dump(exclude_unset=True)
        statement: Update = (
            update(self.model)
            .where(self.model.id == id)
            .values(**values)
            .returning(self.model)
        )
        result = await session.execute(statement)
        await session.flush()
        model_instance = result.scalar_one()
        return self._to_schema(model_instance)

    async def delete(self, session: AsyncSession, id: int) -> None:
        statement = delete(self.model).where(self.model.id == id)
        result = await session.execute(statement)
        if not result.rowcount:
            raise ValueError(f"Entity {self.model} with id {id} not found.")

    async def get_by_id(self, session: AsyncSession, id: int) -> ResponseSchemaT | None:
        statement = select(self.model).where(self.model.id == id)
        result = await session.execute(statement)
        model_instance = result.scalar_one_or_none()
        return self._to_schema(model_instance)

    async def get_many(
        self,
        session: AsyncSession,
        limit: int = 100,
        offset: int = 0,
        **filters,
    ) -> list[ResponseSchemaT]:
        statement = select(self.model).filter_by(**filters).offset(offset).limit(limit)
        result = await session.execute(statement)
        model_instances = result.scalars().all()
        return [self._to_schema(m) for m in model_instances]

    async def get_many_by_ids(
        self, session: AsyncSession, ids: list[int]
    ) -> list[ResponseSchemaT]:
        statement = select(self.model).where(self.model.id.in_(ids))
        result = await session.execute(statement)
        model_instances = result.scalars().all()
        return [self._to_schema(m) for m in model_instances]

    async def get_one_or_none(
        self, session: AsyncSession, **filters
    ) -> ResponseSchemaT | None:
        statement = select(self.model).filter_by(**filters)
        result = await session.execute(statement)
        model_instance = result.scalar_one_or_none()
        return self._to_schema(model_instance)


class AlchSoftDeleteRepository(
    Generic[SoftDeleteModelT, CreateSchemaT, UpdateSchemaT, ResponseSchemaT]
):
    def __init__(
        self,
        model: type[SoftDeleteModelT],
        response_schema: type[ResponseSchemaT],
    ):
        self._model = model
        self._response_schema = response_schema
        if "disabled" not in model.__dict__:
            raise TypeError(
                f"Model {model.__tablename__} doesn't have 'disabled' "
                "field. Use AlchRepository instead."
            )

    @property
    def model(self) -> type[SoftDeleteModelT]:
        return self._model

    @property
    def response_schema(self) -> type[ResponseSchemaT]:
        return self._response_schema

    def _apply_disabled_filter(
        self, statement: Update | Insert | Select | Delete
    ) -> Delete | Update | Select | Any | Insert:
        if hasattr(self.model, "disabled"):
            return statement.where(not_(self.model.disabled))
        return statement

    async def create(
        self, session: AsyncSession, data: CreateSchemaT
    ) -> ResponseSchemaT:
        entity_data = data.model_dump()
        statement: Insert = (
            insert(self.model).values(**entity_data).returning(self.model)
        )
        result = await session.execute(statement)
        await session.flush()
        model_instance = result.scalar_one()
        return self._to_schema(model_instance)

    async def update(
        self, session: AsyncSession, id: int, data: UpdateSchemaT
    ) -> ResponseSchemaT:
        values = data.model_dump(exclude_unset=True)
        if not values:
            raise ValueError("At least one field must be provided")
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
        return self._to_schema(model_instance)

    async def delete(self, session: AsyncSession, id: int) -> None:
        statement = delete(self.model).where(self.model.id == id)
        result = await session.execute(statement)
        if not result.rowcount:
            raise ValueError(f"Entity {self.model} with id {id} not found.")

    async def get_by_id(self, session: AsyncSession, id: int) -> ResponseSchemaT | None:
        statement = select(self.model).where(self.model.id == id)
        statement = self._apply_disabled_filter(statement)
        result = await session.execute(statement)
        model_instance = result.scalar_one_or_none()
        return self._to_schema(model_instance)

    async def get_many(
        self,
        session: AsyncSession,
        limit: int = 100,
        offset: int = 0,
        **filters,
    ) -> list[ResponseSchemaT]:
        statement = select(self.model).filter_by(**filters).offset(offset).limit(limit)
        statement = self._apply_disabled_filter(statement)
        result = await session.execute(statement)
        model_instances = result.scalars().all()
        return [self._to_schema(m) for m in model_instances]

    async def get_many_by_ids(
        self, session: AsyncSession, ids: list[int]
    ) -> list[ResponseSchemaT]:
        statement = select(self.model).where(self.model.id.in_(ids))
        statement = self._apply_disabled_filter(statement)
        result = await session.execute(statement)
        model_instances = result.scalars().all()
        return [self._to_schema(m) for m in model_instances]

    async def get_one_or_none(
        self, session: AsyncSession, **filters
    ) -> ResponseSchemaT | None:
        statement = select(self.model).filter_by(**filters)
        statement = self._apply_disabled_filter(statement)
        result = await session.execute(statement)
        model_instance = result.scalar_one_or_none()
        return self._to_schema(model_instance)

    async def _update_attr(
        self,
        session: AsyncSession,
        id: int,
        value: Any,
    ) -> None:
        statement = (
            update(self.model)
            .where(self.model.id == id)
            .values({getattr(self.model, self._deleted_column_name): value})
        )
        result = await session.execute(statement)
        if not result.rowcount:
            raise ValueError(f"Entity {self.model} with id {id} not found.")

    async def soft_delete(self, session: AsyncSession, id: int) -> None:
        await self._update_attr(session=session, id=id, value=True)

    async def soft_restore(self, session: AsyncSession, id: int) -> None:
        await self._update_attr(session=session, id=id, value=False)

    async def get_archived_list(
        self,
        session: AsyncSession,
        limit: int = 100,
        offset: int = 0,
        **filters,
    ) -> list[ResponseSchemaT]:
        statement = (
            select(self.model)
            .filter_by(**filters)
            .offset(offset)
            .limit(limit)
            .where(getattr(self.model, self._deleted_column_name))
        )
        result = await session.execute(statement)
        model_instances = result.scalars().all()
        return [self._to_schema(m) for m in model_instances]

    async def get_archived(
        self, session: AsyncSession, **filters
    ) -> ResponseSchemaT | None:
        statement = (
            select(self.model)
            .filter_by(**filters)
            .where(getattr(self.model, self._deleted_column_name))
        )
        result = await session.execute(statement)
        model_instance = result.scalar_one_or_none()
        return self._to_schema(model_instance)

    def _to_schema(self, model_instance: ModelT | None) -> ResponseSchemaT | None:
        if model_instance is None:
            return None
        return self.response_schema.model_validate(model_instance)
