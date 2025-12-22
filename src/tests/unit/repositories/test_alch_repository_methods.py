import pytest
from conftest import (
    CreateSchema,
    Model,
    ResponseSchema,
    UpdateSchema,
)
from sqlalchemy import select


class TestAlchRepository:
    """Тесты для AlchRepository"""

    @pytest.mark.anyio
    async def test_create_success(self, test_repository, db_session):
        """Тест успешного создания записи"""
        create_data = CreateSchema(
            name="John Doe", email="john@example.com"
        )

        await test_repository.create(db_session, create_data)
        await db_session.commit()

        result = await db_session.execute(
            select(Model).where(Model.email == "john@example.com")
        )
        created = result.scalar_one_or_none()

        assert created is not None
        assert created.name == "John Doe"
        assert created.email == "john@example.com"

    @pytest.mark.anyio
    async def test_get_by_id_success(self, test_repository, db_session):
        """Тест получения записи по ID"""
        test_model = Model(name="Test", email="test@example.com")
        db_session.add(test_model)
        await db_session.commit()
        await db_session.refresh(test_model)

        result = await test_repository.get_by_id(db_session, test_model.id)

        assert result is not None
        assert result.id == test_model.id
        assert result.name == "Test"
        assert isinstance(result, ResponseSchema)

    @pytest.mark.anyio
    async def test_get_by_id_not_found(self, test_repository, db_session):
        """Тест получения несуществующей записи"""
        result = await test_repository.get_by_id(db_session, 999999)

        assert result is None

    @pytest.mark.anyio
    async def test_update_success(self, test_repository, db_session):
        """Тест успешного обновления"""
        test_model = Model(name="Old", email="old@example.com")
        db_session.add(test_model)
        await db_session.commit()
        await db_session.refresh(test_model)

        update_data = UpdateSchema(name="Updated")

        await test_repository.update(db_session, test_model.id, update_data)
        await db_session.commit()

        result = await test_repository.get_by_id(db_session, test_model.id)
        assert result.name == "Updated"
        assert result.email == "old@example.com"

    @pytest.mark.anyio
    async def test_update_not_found(self, test_repository, db_session):
        """Тест обновления несуществующей записи"""
        update_data = UpdateSchema(name="Updated")

        with pytest.raises(ValueError, match="not found"):
            await test_repository.update(db_session, 999999, update_data)

    @pytest.mark.anyio
    async def test_delete_success(self, test_repository, db_session):
        """Тест успешного удаления"""
        test_model = Model(name="ToDelete", email="delete@example.com")
        db_session.add(test_model)
        await db_session.commit()
        await db_session.refresh(test_model)

        await test_repository.delete(db_session, test_model.id)
        await db_session.commit()

        result = await test_repository.get_by_id(db_session, test_model.id)
        assert result is None

    @pytest.mark.anyio
    async def test_delete_not_found(self, test_repository, db_session):
        """Тест удаления несуществующей записи"""
        with pytest.raises(ValueError, match="not found"):
            await test_repository.delete(db_session, 999999)

    @pytest.mark.anyio
    async def test_get_many(self, test_repository, db_session):
        """Тест получения нескольких записей"""
        models = [
            Model(name=f"User{i}", email=f"user{i}@example.com")
            for i in range(5)
        ]
        db_session.add_all(models)
        await db_session.commit()

        results = await test_repository.get_many(
            db_session, limit=10, offset=0
        )

        assert len(results) == 5
        assert all(isinstance(r, ResponseSchema) for r in results)
        assert {r.name for r in results} == {f"User{i}" for i in range(5)}

    @pytest.mark.anyio
    async def test_get_many_with_filters(self, test_repository, db_session):
        """Тест получения с фильтрами"""
        models = [
            Model(name="Alice", email="alice@example.com"),
            Model(name="Bob", email="bob@example.com"),
            Model(name="Alice", email="alice2@example.com"),
        ]
        db_session.add_all(models)
        await db_session.commit()

        results = await test_repository.get_many(
            db_session, name="Alice", limit=10
        )

        assert len(results) == 2
        assert all(r.name == "Alice" for r in results)

    @pytest.mark.anyio
    async def test_get_many_by_ids(self, test_repository, db_session):
        """Тест получения по списку ID"""
        models = [
            Model(name=f"User{i}", email=f"user{i}@example.com")
            for i in range(10)
        ]
        db_session.add_all(models)
        await db_session.commit()
        await db_session.refresh(models[0])
        await db_session.refresh(models[2])
        await db_session.refresh(models[4])

        results = await test_repository.get_many_by_ids(
            db_session,
            ids=[
                models[0].id,
                models[2].id,
                models[4].id,
                999999,
            ],
        )

        assert len(results) == 3
        ids = {r.id for r in results}
        assert ids == {models[0].id, models[2].id, models[4].id}

    @pytest.mark.anyio
    async def test_get_one_or_none_not_found(
        self, test_repository, db_session
    ):
        """Тест получения одной записи или None (не найдено)"""
        result = await test_repository.get_one_or_none(
            db_session, email="nonexistent@example.com"
        )

        assert result is None

    @pytest.mark.anyio
    async def test_get_one_or_none_found(self, test_repository, db_session):
        """Тест получения одной записи"""
        test_model = Model(name="Unique", email="unique@example.com")
        db_session.add(test_model)
        await db_session.commit()
        await db_session.refresh(test_model)

        result = await test_repository.get_one_or_none(
            db_session, email="unique@example.com"
        )

        assert result is not None
        assert result.id == test_model.id
        assert result.email == "unique@example.com"

    @pytest.mark.anyio
    async def test_to_schema_with_model(self, test_repository):
        """Тест преобразования модели в схему"""
        model_instance = Model(id=1, name="Test", email="test@example.com")

        result = test_repository._to_schema(model_instance)

        assert isinstance(result, ResponseSchema)
        assert result.id == 1
        assert result.name == "Test"

    @pytest.mark.anyio
    async def test_to_schema_with_none(self, test_repository):
        """Тест преобразования None в схему"""
        result = test_repository._to_schema(None)

        assert result is None
