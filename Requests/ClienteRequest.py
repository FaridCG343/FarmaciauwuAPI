import pydantic
from pydantic import BaseModel
from typing import Optional
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
    def validarTelefono(cls, value):
        if re.search("[0-9]{3}(-| )[0-9]{3}(-| )[0-9]{2}(-| )[0-9]{2}", value) is None:
            raise HTTPException(400, "El telefono debe tener el siguiente formato 999-999-99-99")
        return value

    @pydantic.validator("correo")
    @classmethod
    def validarCorreo(cls, value):
        if re.search("[a-zA-Z0-9]+@[a-zA-Z]+[.].+", value) is None:
            raise HTTPException(400, "El correo debe ser valido")
        return value
