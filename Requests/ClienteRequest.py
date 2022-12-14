from pydantic import BaseModel, ValidationError, validator
from pydantic.typing import Optional
from fastapi import HTTPException
import re


class ClienteRequest(BaseModel):
    nombre: str
    apellidos: str
    telefono: str
    correo: Optional[str] = None
    direccion: Optional[str] = None


    @classmethod
    def phone_validate(cls, value):
        if re.search("^[0-9]{3}(-| )[0-9]{3}(-| )[0-9]{2}(-| )[0-9]{2}$", value) is None:
            raise ValidationError("The phone-number must be like 999-999-99-99")
        return value


    @classmethod
    def email_validate(cls, value):
        if re.search("[a-zA-Z0-9]+@[a-zA-Z]+[.].+", value) is None:
            raise ValidationError("The email must be valid")
        return value


class ClientUpdateRequest(BaseModel):
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    direccion: Optional[str] = None

    @validator("telefono")
    def phone_validate(cls, value):
        if re.search("^[0-9]{3}(-| )[0-9]{3}(-| )[0-9]{2}(-| )[0-9]{2}$", value) is None:
            raise ValidationError("The phone-number must be like 999-999-99-99")
        return value

    @validator("correo")
    def email_validate(cls, value):
        if re.search("[a-zA-Z0-9]+@[a-zA-Z]+[.].+", value) is None:
            raise ValidationError("The email must be valid")
        return value

