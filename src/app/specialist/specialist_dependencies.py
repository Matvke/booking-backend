from fastapi import Depends

from .specialist_model import Specialist
from .specialist_repository import AlchSpecialistRepository, SpecialistRepository
from .specialist_schemas import SpecialistResponseSchema
from .specialist_service import SpecialistService


async def get_specialist_alch_repository() -> SpecialistRepository:
    return AlchSpecialistRepository(Specialist, SpecialistResponseSchema)


async def get_specialist_service(
    repository: SpecialistRepository = Depends(get_specialist_alch_repository),
) -> SpecialistService:
    return SpecialistService(specialist_repository=repository)
