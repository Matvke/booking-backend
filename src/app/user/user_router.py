from fastapi import APIRouter, Depends, Path

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
    session: UnitOfWork = Depends(get_uow),
    service: UserService = Depends(get_user_service),
) -> UserResponseSchema:
    return await service.create_user(session, user)


@user_router.get(path="/{user_telegram_id}")
async def get_user_by_id(
    user: UserResponseSchema = Depends(get_current_user),
) -> UserResponseSchema:
    return user


@user_router.put(path="/{user_telegram_id}")
async def update_user(
    user_data: UserUpdateSchema,
    user_telegram_id: str = Path(
        min_length=10, max_length=10, pattern=r"^[1-9]\d{9}$"
    ),
    session: UnitOfWork = Depends(get_uow),
    service: UserService = Depends(get_user_service),
) -> UserResponseSchema:
    user = await service.get_user_by_telegram_id(session, user_telegram_id)
    return await service.update_user(session, user.id, user_data)
