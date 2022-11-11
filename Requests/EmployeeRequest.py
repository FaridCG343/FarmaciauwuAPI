from pydantic import BaseModel
from pydantic.typing import Optional
import pydantic
import re
from fastapi import HTTPException


class Employee(BaseModel):
    nombre: str
    apellidos: str
    telefono: Optional[str] = None

    @classmethod
    @pydantic.validator("telefono")
    def phone_validate(cls, value):
        if re.search("[0-9]{3}(-| )[0-9]{3}(-| )[0-9]{2}(-| )[0-9]{2}", value) is None:
            raise HTTPException(400, "The phone-number must be like 999-999-99-99")
        return value


class EmployeeAuth(BaseModel):
    id: int
    password: str
    admin: Optional[bool] = 0
