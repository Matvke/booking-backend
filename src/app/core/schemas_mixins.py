from pydantic import BaseModel, AwareDatetime, ConfigDict


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


class TimestampDisabledSchemaMixin(
    TimestampSchemaMixin, DisabledSchemaMixin, BaseModel
):
    pass
