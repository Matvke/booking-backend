from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schemas import (
    CreateSchema,
    ResponseSchema,
    RussianPhoneNumber,
    UpdateSchema,
)
from app.core.enums import UserRole
from app.core.schemas_mixins import (
    IDIntSchemaMixin,
    TimestampDisabledSchemaMixin,
)


class UserBaseSchema(BaseModel):
    pass


class UserCreateSchema(CreateSchema, UserBaseSchema):
    telegram_id: str = Field(min_length=10, max_length=10, pattern=r"^[1-9]\d{9}$")


class UserUpdateSchema(UpdateSchema, UserBaseSchema):
    phone_number: RussianPhoneNumber | None = None
    name: str | None = Field(default=None, max_length=50, min_length=1)


class UserResponseSchema(
    ResponseSchema,
    IDIntSchemaMixin,
    TimestampDisabledSchemaMixin,
):
    telegram_id: str
    phone_number: str | None = None
    name: str | None = None
    role: UserRole

    model_config = ConfigDict(from_attributes=True, strict=True)


class UserListResponseSchema(BaseModel):
    items: list[UserResponseSchema]
    total: int
    limit: int
    offset: int
