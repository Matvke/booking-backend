from unittest.mock import AsyncMock

import pytest
from conftest import (
    CreateSchema,
    Model,
    ResponseSchema,
    SoftDeleteModel,
    UpdateSchema,
)
from sqlalchemy.exc import (
    IntegrityError,
    MultipleResultsFound,
    SQLAlchemyError,
)


class TestAlchRepositoryErrors:
    """Тесты обработки ошибок"""

    @pytest.mark.anyio
    async def test_create_integrity_error(self, test_repository):
        """Тест обработки IntegrityError при создании"""
        mock_session = AsyncMock()
        mock_session.execute.side_effect = IntegrityError(
            "UNIQUE constraint failed", {}, None
        )

        create_data = CreateSchema(name="Test", email="test@example.com")

        with pytest.raises(IntegrityError):
            await test_repository.create(mock_session, create_data)

    @pytest.mark.anyio
    async def test_update_database_error(self, test_repository):
        """Тест обработки ошибок БД при обновлении"""
        mock_session = AsyncMock()
        mock_session.execute.side_effect = SQLAlchemyError("DB error")

        update_data = UpdateSchema(name="Updated")

        with pytest.raises(SQLAlchemyError):
            await test_repository.update(mock_session, 1, update_data)

    @pytest.mark.anyio
    async def test_with_soft_delete_model_raises_error(self):
        """Тест что модель с disabled вызывает ошибку"""
        from app.core.implementations.sqlalchemy_repository import (
            AlchRepository,
        )

        with pytest.raises(TypeError, match="has 'disabled' field"):
            AlchRepository(
                model=SoftDeleteModel, response_schema=ResponseSchema
            )

    @pytest.mark.anyio
    async def test_get_one_or_none_multiple_found(
        self, test_repository, db_session
    ):
        """Тест получения когда несколько записей подходят"""
        models = [
            Model(name="Duplicate", email="dup1@example.com"),
            Model(name="Duplicate", email="dup2@example.com"),
        ]
        db_session.add_all(models)
        await db_session.commit()

        with pytest.raises(MultipleResultsFound):
            await test_repository.get_one_or_none(db_session, name="Duplicate")
