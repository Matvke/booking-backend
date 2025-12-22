import pytest
import pytest_asyncio
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Model(Base):
    __tablename__ = "test_model"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))


class SoftDeleteModel(Base):
    __tablename__ = "test_softdelete_model"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    disabled = Column(Integer, default=0)


class CreateSchema(BaseModel):
    name: str
    email: str


class UpdateSchema(BaseModel):
    name: str | None = None
    email: str | None = None


class ResponseSchema(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


@pytest_asyncio.fixture
async def db_session():
    """Тестовая сессия БД в памяти"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    session = async_session()
    try:
        yield session
    finally:
        await session.close()

        await engine.dispose()


@pytest.fixture
def test_repository():
    """Фикстура репозитория"""
    from app.core.implementations.sqlalchemy_repository import AlchRepository

    class TestRepository(
        AlchRepository[Model, CreateSchema, UpdateSchema, ResponseSchema]
    ):
        pass

    return TestRepository(model=Model, response_schema=ResponseSchema)
