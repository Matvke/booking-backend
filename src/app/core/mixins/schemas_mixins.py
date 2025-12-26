from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class IDIntSchemaMixin(BaseModel):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class TimestampSchemaMixin(BaseModel):
    created_at: AwareDatetime
    updated_at: AwareDatetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class DisabledSchemaMixin(BaseModel):
    disabled: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


class TelegramIDMixin(BaseModel):
    telegram_id: str = Field(min_length=10, max_length=10, pattern=r"^[1-9]\d{9}$")


class TimestampDisabledSchemaMixin(
    TimestampSchemaMixin, DisabledSchemaMixin, BaseModel
):
    pass
