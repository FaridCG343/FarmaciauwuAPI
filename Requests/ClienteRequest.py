import pydantic
from pydantic import BaseModel
from pydantic.typing import Optional
from fastapi import HTTPException
import re


class ClienteRequest(BaseModel):
    nombre: str
    apellidos: str
    telefono: str
    correo: Optional[str] = None
    direccion: Optional[str] = None


    @pydantic.validator("telefono")
    @classmethod
    def phone_validate(cls, value):
        if re.search("[0-9]{3}(-| )[0-9]{3}(-| )[0-9]{2}(-| )[0-9]{2}", value) is None:
            raise HTTPException(400, "The phone-number must be like 999-999-99-99")
        return value


    @pydantic.validator("correo")
    @classmethod
    def email_validate(cls, value):
        if re.search("[a-zA-Z0-9]+@[a-zA-Z]+[.].+", value) is None:
            raise HTTPException(400, "The email must be valid")
        return value


class ClientUpdateRequest(BaseModel):
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    direccion: Optional[str] = None

    @classmethod
    @pydantic.validator("telefono")
    def phone_validate(cls, value):
        if re.search("[0-9]{3}(-| )[0-9]{3}(-| )[0-9]{2}(-| )[0-9]{2}", value) is None:
            raise HTTPException(400, "The phone-number must be like 999-999-99-99")
        return value

    @classmethod
    @pydantic.validator("correo")
    def email_validate(cls, value):
        if re.search("[a-zA-Z0-9]+@[a-zA-Z]+[.].+", value) is None:
            raise HTTPException(400, "The email must be valid")
        return value

