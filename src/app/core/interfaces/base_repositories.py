from abc import abstractmethod
from typing import Generic, Protocol, TypeVar, runtime_checkable

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base


CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)
ResponseSchemaT = TypeVar("ResponseSchemaT", bound=BaseModel)

ModelT = TypeVar("ModelT", bound=Base)
SoftDeleteModelT = TypeVar("SoftDeleteModelT", bound=Base)


@runtime_checkable
class Repository(
    Protocol, Generic[ModelT, CreateSchemaT, UpdateSchemaT, ResponseSchemaT]
):
    """Репозиторий с базовыми CRUD операциями
    для моделей без мягкого удаления"""

    @property
    @abstractmethod
    def model(self) -> type[ModelT]:
        """Модель БД"""

    @property
    @abstractmethod
    def response_schema(self) -> type[ResponseSchemaT]:
        """Схема ответа"""

    @abstractmethod
    async def create(
        self, session: AsyncSession, data: CreateSchemaT
    ) -> ResponseSchemaT:
        """
        Создать объект в БД. Не применяет commit.

        :param data: Create Pydantic схема
        :type data: CreateSchemaT
        """

    @abstractmethod
    async def update(
        self, session: AsyncSession, id: int, data: UpdateSchemaT
    ) -> ResponseSchemaT:
        """
        Обновить любой объект по id, исключая архивные. Не применяет commit.

        :param id: id объекта в БД
        :type id: int
        :param data: Update Pydantic схема
        :type data: UpdateSchemaT
        """

    @abstractmethod
    async def delete(self, session: AsyncSession, id: int) -> None:
        """
        Удалиить любой объект по id. Не применяет commit.

        :param id: id объекта в БД
        :type id: int
        """

    @abstractmethod
    async def get_by_id(self, session: AsyncSession, id: int) -> ResponseSchemaT | None:
        """
        Получить любой объект по id, исключая архивные

        :param id: id объекта в БД
        :type id: int
        :return: Response Pydantic схема
        :rtype: ResponseSchemaT | None
        """

    @abstractmethod
    async def get_many(
        self,
        session: AsyncSession,
        limit: int = 100,
        offset: int = 0,
        **filters,
    ) -> list[ResponseSchemaT]:
        """
        Получить список объектов, исключая архивные

        :param limit: Длина полученного списка
        :type limit: int
        :param offset: Отступ от начала списка
        :type offset: int
        :param filters: Фильтры для поиска объектов в БД,
        передаются как именованные параметры (например, `name='John'`)
        :return: Список Response Pydantic схем
        :rtype: list[ResponseSchemaT]
        """

    @abstractmethod
    async def get_many_by_ids(
        self, session: AsyncSession, ids: list[int]
    ) -> list[ResponseSchemaT]:
        """
        Получить список объектов, исключая архивные

        :param ids: Список id
        :type ids: list[int]
        :return: Response Pydantic схема
        :rtype: list[ResponseSchemaT]
        """

    @abstractmethod
    async def get_one_or_none(
        self, session: AsyncSession, **filters
    ) -> ResponseSchemaT | None:
        """
        Получить объект по фильтрам, исключая архивные. Выкидывает ошибку
        MultipleResultsFound если в результате больше 1 объекта.

        :param filters: Фильтры для поиска объектов в БД,
        передаются как именованные параметры (например, `name='John'`)
        :return: Response Pydantic схема
        :rtype: ResponseSchemaT | None
        """

    @abstractmethod
    def _to_schema(self, model_instance: ModelT | None) -> ResponseSchemaT | None:
        """Привести модель БД к схеме"""


@runtime_checkable
class SoftDeleteRepository(
    Protocol,
    Generic[SoftDeleteModelT, CreateSchemaT, UpdateSchemaT, ResponseSchemaT],
):
    """Репозиторий для моделей с мягким удалением"""

    @property
    @abstractmethod
    def model(self) -> type[SoftDeleteModelT]:
        """Модель БД"""

    @property
    @abstractmethod
    def response_schema(self) -> type[ResponseSchemaT]:
        """Схема ответа"""

    @abstractmethod
    async def create(
        self, session: AsyncSession, data: CreateSchemaT
    ) -> ResponseSchemaT:
        """
        Создать объект в БД. Не применяет commit.

        :param data: Create Pydantic схема
        :type data: CreateSchemaT
        """

    @abstractmethod
    async def update(
        self, session: AsyncSession, id: int, data: UpdateSchemaT
    ) -> ResponseSchemaT:
        """
        Обновить любой объект по id. Не применяет commit.

        :param id: id объекта в БД
        :type id: int
        :param data: Update Pydantic схема
        :type data: UpdateSchemaT
        """

    @abstractmethod
    async def delete(self, session: AsyncSession, id: int) -> None:
        """
        Удалиить любой объект по id. Не применяет commit.

        :param id: id объекта в БД
        :type id: int
        """

    @abstractmethod
    async def get_by_id(self, session: AsyncSession, id: int) -> ResponseSchemaT | None:
        """
        Получить любой объект по id, исключая архивные.

        :param id: id объекта в БД
        :type id: int
        :return: Response Pydantic схема
        :rtype: ResponseSchemaT | None
        """

    @abstractmethod
    async def get_many(
        self,
        session: AsyncSession,
        limit: int = 100,
        offset: int = 0,
        **filters,
    ) -> list[ResponseSchemaT]:
        """
        Получить список объектов, исключая архивные.

        :param limit: Длина полученного списка
        :type limit: int
        :param offset: Отступ от начала списка
        :type offset: int
        :param filters: Фильтры для поиска объектов в БД,
        передаются как именованные параметры (например, `name='John'`)
        :return: Список Response Pydantic схем
        :rtype: list[ResponseSchemaT]
        """

    @abstractmethod
    async def get_many_by_ids(
        self, session: AsyncSession, ids: list[int]
    ) -> list[ResponseSchemaT]:
        """
        Получить список объектов, исключая архивные.

        :param ids: Список id
        :type ids: list[int]
        :return: Response Pydantic схема
        :rtype: list[ResponseSchemaT]
        """

    @abstractmethod
    async def get_one_or_none(
        self, session: AsyncSession, **filters
    ) -> ResponseSchemaT | None:
        """
        Получить объект по фильтрам, исключая архивные. Выкидывает ошибку
        MultipleResultsFound если в результате больше 1 объекта.

        :param filters: Фильтры для поиска объектов в БД,
        передаются как именованные параметры (например, `name='John'`)
        :return: Response Pydantic схема
        :rtype: ResponseSchemaT | None
        """

    @abstractmethod
    async def soft_delete(self, session: AsyncSession, id: int) -> None:
        """
        Поместить объект в архив. Не применяет commit.

        :param id: id объекта в БД
        :type id: int
        """

    @abstractmethod
    async def soft_restore(self, session: AsyncSession, id: int) -> None:
        """
        Восстановить из архива. Не применяет commit.

        :param id: id объекта в БД
        :type id: int
        """

    @abstractmethod
    async def get_archived_list(
        self,
        session: AsyncSession,
        limit: int = 100,
        offset: int = 0,
        **filters,
    ) -> list[ResponseSchemaT]:
        """
        Получить список объектов из архива.

        :param limit: Длина полученного списка
        :type limit: int
        :param offset: Отступ от начала списка
        :type offset: int
        :param filters: Фильтры для поиска объектов в БД,
        передаются как именованные параметры (например, `name='John'`)
        :return: Список Response Pydantic схем
        :rtype: list[ResponseSchemaT]
        """

    @abstractmethod
    async def get_archived(
        self, session: AsyncSession, **filters
    ) -> ResponseSchemaT | None:
        """
        Получить объект из архива. Выкидывает ошибку
        MultipleResultsFound если в результате больше 1 объекта.

        :param filters: Фильтры для поиска объектов в БД,
        передаются как именованные параметры (например, `name='John'`)
        :return: Response Pydantic схема
        :rtype: ResponseSchemaT | None
        """

    @abstractmethod
    def _to_schema(
        self, model_instance: SoftDeleteModelT | None
    ) -> ResponseSchemaT | None:
        """Привести модель БД к схеме"""
