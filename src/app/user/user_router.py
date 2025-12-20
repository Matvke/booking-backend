from fastapi import APIRouter, Depends

from app.core.dependencies import get_uow
from app.core.implementations.uow import UnitOfWork

from .user_dependencies import get_current_user, get_user_service
from .user_schemas import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)
from .user_service import UserService

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@user_router.post(path="")
async def create_user(
    user: UserCreateSchema,
    uow: UnitOfWork = Depends(get_uow),
    service: UserService = Depends(get_user_service),
) -> UserResponseSchema:
    async with uow.session.begin():
        user = await service.create_user(uow.session, user)
        return user


@user_router.get(path="/{user_id}")
async def get_user_by_id(
    user_id: int,
    uow: UnitOfWork = Depends(get_uow),
    user: UserResponseSchema = Depends(get_current_user),
) -> UserResponseSchema:
    return user


@user_router.put(path="/{user_id}")
async def update_user(
    user_id: int,
    user_data: UserUpdateSchema,
    uow: UnitOfWork = Depends(get_uow),
    service: UserService = Depends(get_user_service),
) -> UserResponseSchema:
    async with uow.session.begin():
        return await service.update_user(uow.session, user_id, user_data)
