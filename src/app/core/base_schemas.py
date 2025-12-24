from pydantic import BaseModel, ConfigDict, model_validator
from pydantic_extra_types.phone_numbers import PhoneNumber


class CreateSchema(BaseModel):
    pass


class UpdateSchema(BaseModel):
    @model_validator(mode="after")
    def check_at_least_one_field_present(self):
        model_fields = self.__class__.model_fields
        provided_fields = 0

        for field_name in model_fields:
            field_value = getattr(self, field_name, None)
            if field_value is not None:
                provided_fields += 1

        if provided_fields == 0:
            raise ValueError("At least one field must be provided for update")

        return self


class ResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)


class RussianPhoneNumber(PhoneNumber):
    default_region_code = "RU"
    supported_regions = ["RU"]
    phone_format = "INTERNATIONAL"
