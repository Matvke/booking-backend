from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_session
from app.user.user_dependencies import get_user_service
from app.user.user_schemas import UserResponseSchema
from app.user.user_service import UserService

from .specialist_dependencies import get_specialist_service
from .specialist_schemas import (
    SpecialistCreateSchema,
    SpecialistInviteCode,
    SpecialistResponseSchema,
    SpecialistUpdateSchema,
)
from .specialist_service import SpecialistService

specialist_router = APIRouter(
    prefix="/specialists",
    tags=["specialists"],
)


@specialist_router.post(path="")
async def create_specialist(
    specialist: SpecialistCreateSchema,
    session: AsyncSession = Depends(get_session),
    service: SpecialistService = Depends(get_specialist_service),
) -> SpecialistResponseSchema:
    return await service.create_specialist(session, specialist)


@specialist_router.get(path="/{specialist_id}")
async def get_specialist_by_id(
    specialist_id: int = Path(...),
    session: AsyncSession = Depends(get_session),
    service: SpecialistService = Depends(get_specialist_service),
) -> SpecialistResponseSchema:
    specialist = await service.get_specialist_by_id(session, specialist_id)
    return specialist


@specialist_router.put(path="/{specialist_id}")
async def update_specialist(
    specialist_data: SpecialistUpdateSchema,
    specialist_id: int = Path(...),
    session: AsyncSession = Depends(get_session),
    service: SpecialistService = Depends(get_specialist_service),
) -> SpecialistResponseSchema:
    specialist = await service.get_specialist_by_id(session, specialist_id)
    return await service.update_specialist(session, specialist.id, specialist_data)


@specialist_router.get(path="/invite_token/{specialist_id}")
async def get_invite_token(
    specialist_id: int = Path(...),
    session: AsyncSession = Depends(get_session),
    specialist_service: SpecialistService = Depends(get_specialist_service),
) -> str:
    return await specialist_service.get_invoke_token(session, specialist_id)


@specialist_router.post(path="/invite_token/{specialist_id}")
async def create_invite_token(
    specialist_id: int = Path(...),
    session: AsyncSession = Depends(get_session),
    specialist_service: SpecialistService = Depends(get_specialist_service),
) -> str:
    return await specialist_service.create_invoke_token(session, specialist_id)


@specialist_router.delete(path="/invite_token/{specialist_id}")
async def delete_invite_token(
    specialist_id: int = Path(...),
    session: AsyncSession = Depends(get_session),
    specialist_service: SpecialistService = Depends(get_specialist_service),
) -> str:
    return await specialist_service.delete_invoke_token(session, specialist_id)


@specialist_router.post(path="/{specialist_id}")
async def register_specialist(
    specialist_data: SpecialistInviteCode,
    specialist_id: int = Path(...),
    session: AsyncSession = Depends(get_session),
    specialist_service: SpecialistService = Depends(get_specialist_service),
    user_service: UserService = Depends(get_user_service),
) -> SpecialistResponseSchema:
    user = await user_service.get_user_by_telegram_id(
        session, specialist_data.telegram_id
    )
    await specialist_service.verify_invoke_token(
        session, specialist_id, specialist_data.invoke_token
    )
    specialist = await specialist_service.update_specialist(
        session, specialist_id, SpecialistUpdateSchema(user_id=user.id)
    )
    await specialist_service.delete_invoke_token(session, specialist_id)
    return specialist


@specialist_router.get(path="/{specialist_id}/user")
async def get_specialist_user(
    specialist_id: int = Path(...),
    session: AsyncSession = Depends(get_session),
    specialist_service: SpecialistService = Depends(get_specialist_service),
    user_service: UserService = Depends(get_user_service),
) -> UserResponseSchema:
    telegram_id = await specialist_service.get_telegram_id(session, specialist_id)
    user = await user_service.get_user_by_telegram_id(session, telegram_id)
    return user
