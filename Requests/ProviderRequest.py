from pydantic import BaseModel, validator, ValidationError
from pydantic.typing import Optional
import re


class ProviderRequest(BaseModel):
    name: str
    phoneNumber: str
    email: str

    @validator("phoneNumber")
    def phone_validate(cls, value):
        if re.search("[0-9]{3}(-| )[0-9]{3}(-| )[0-9]{2}(-| )[0-9]{2}", value) is None:
            raise ValidationError("The phone-number must be like 999-999-99-99")
        return value

    @validator("email")
    def email_validate(cls, value):
        if re.search("[a-zA-Z0-9]+@[a-zA-Z]+[.].+", value) is None:
            raise ValidationError("The email must be valid")
        return value


class ProviderUpdateRequest(BaseModel):
    name: Optional[str] = None
    phoneNumber: Optional[str] = None
    email: Optional[str] = None

    @validator("phoneNumber")
    def phone_validate(cls, value):
        if re.search("[0-9]{3}(-| )[0-9]{3}(-| )[0-9]{2}(-| )[0-9]{2}", value) is None:
            raise ValidationError(400, "The phone-number must be like 999-999-99-99")
        return value

    @validator("email")
    def email_validate(cls, value):
        if re.search("[a-zA-Z0-9]+@[a-zA-Z]+[.].+", value) is None:
            raise ValidationError(400, "The email must be valid")
        return value