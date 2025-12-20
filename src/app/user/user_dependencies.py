from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_session
from app.user.user_schemas import UserResponseSchema

from .user_model import User
from .user_repository import AlchUserRepository, UserRepository
from .user_service import UserService


async def get_user_alch_repository() -> UserRepository:
    return AlchUserRepository(User, UserResponseSchema)


async def get_user_service(
    repository: UserRepository = Depends(get_user_alch_repository),
) -> UserService:
    return UserService(user_repository=repository)


async def get_current_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    service: UserService = Depends(get_user_service),
) -> User:
    async with session.begin():
        user = await service.get_user_by_id(session, user_id)
        return user
