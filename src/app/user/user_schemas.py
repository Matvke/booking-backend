from pydantic import BaseModel, Field, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.core.schemas_mixins import (
    IDIntSchemaMixin,
    TimestampDisabledSchemaMixin,
)


class UserBaseSchema(BaseModel):
    pass


class UserCreateSchema(UserBaseSchema):
    telegram_id: str = Field(
        min_length=10, max_length=10, pattern=r"^[1-9]\d{9}$"
    )


class UserUpdateSchema(UserBaseSchema):
    # TODO: Не принимает номера начинающиеся с 8
    phone_number: PhoneNumber | None = None
    name: str | None = Field(default=None, max_length=50, min_length=1)


class UserResponseSchema(
    IDIntSchemaMixin,
    TimestampDisabledSchemaMixin,
):
    telegram_id: str
    phone_number: str | None = None
    name: str | None = None

    model_config = ConfigDict(from_attributes=True, strict=True)


class UserListResponseSchema(BaseModel):
    items: list[UserResponseSchema]
    total: int
    limit: int
    offset: int
