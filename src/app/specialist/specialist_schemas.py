from pydantic import BaseModel, Field

from app.core.base_schemas import CreateSchema, ResponseSchema, UpdateSchema
from app.core.enums import SpecialistStatus
from app.core.mixins.schemas_mixins import (
    IDIntSchemaMixin,
    TelegramIDMixin,
    TimestampDisabledSchemaMixin,
)


class SpecialistBaseSchema(BaseModel):
    pass


class SpecialistCreateSchema(CreateSchema, SpecialistBaseSchema):
    user_id: int | None = None
    name: str = Field(min_length=2, max_length=50)
    speciality: str | None = Field(default=None, min_length=2, max_length=50)


class SpecialistUpdateSchema(UpdateSchema, SpecialistBaseSchema):
    user_id: int | None = None
    name: str | None = Field(None, min_length=2, max_length=50)
    speciality: str | None = Field(None, min_length=2, max_length=50)
    specialist_status: SpecialistStatus | None = None


class SpecialistResponseSchema(
    ResponseSchema,
    IDIntSchemaMixin,
    TimestampDisabledSchemaMixin,
):
    name: str
    user_id: int | None
    speciality: str | None
    specialist_status: SpecialistStatus | None


class SpecialistInviteCode(TelegramIDMixin):
    invoke_token: str = Field(min_length=4, max_length=4)


class SpecialistListResponseSchema(BaseModel):
    items: list[SpecialistResponseSchema]
    total: int
    limit: int
    offset: int
