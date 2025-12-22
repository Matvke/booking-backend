from fastapi import Depends, Path
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
    user_telegram_id: str = Path(...),
    session: AsyncSession = Depends(get_session),
    service: UserService = Depends(get_user_service),
) -> User:
    """Зависимости в fastapi вызываются до валидации body."""
    user = await service.get_user_by_telegram_id(session, user_telegram_id)
    return user
