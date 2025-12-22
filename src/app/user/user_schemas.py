from pydantic import BaseModel, Field, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber
from app.core.schemas_mixins import (
    IDIntSchemaMixin,
    TimestampDisabledSchemaMixin,
)


class RussianPhoneNumber(PhoneNumber):
    default_region_code = "RU"
    supported_regions = ["RU"]
    phone_format = "INTERNATIONAL"


class UserBaseSchema(BaseModel):
    pass


class UserCreateSchema(UserBaseSchema):
    telegram_id: str = Field(
        min_length=10, max_length=10, pattern=r"^[1-9]\d{9}$"
    )


class UserUpdateSchema(UserBaseSchema):
    phone_number: RussianPhoneNumber | None = None
    name: str | None = Field(default=..., max_length=50, min_length=1)


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
