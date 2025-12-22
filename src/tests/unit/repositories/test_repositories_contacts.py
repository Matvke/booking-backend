from unittest.mock import Mock

import pytest
from sqlalchemy import Boolean, Column, Integer

from app.core.implementations.sqlalchemy_repository import (
    AlchRepository,
    AlchSoftDeleteRepository,
)
from app.core.interfaces.base_repositories import (
    Repository,
    SoftDeleteRepository,
)


@pytest.mark.anyio
async def test_repository_protocol_contract():
    regular_model_mock = Mock()
    regular_model_mock.__tablename__ = "test_table"
    regular_model_mock.id = Column(Integer, primary_key=True)

    repo = AlchRepository(regular_model_mock, Mock())
    assert isinstance(repo, Repository)


@pytest.mark.anyio
async def test_soft_delete_repository_protocol_contract():
    soft_delete_model_mock = Mock()
    soft_delete_model_mock.__tablename__ = "test_table"
    soft_delete_model_mock.id = Column(Integer, primary_key=True)
    soft_delete_model_mock.disabled = Column(Boolean)

    repo = AlchSoftDeleteRepository(soft_delete_model_mock, Mock())
    assert isinstance(repo, SoftDeleteRepository)
