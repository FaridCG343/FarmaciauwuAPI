from pydantic import BaseModel, ValidationError
from pydantic.typing import Optional
import pydantic
import re
from fastapi import HTTPException


class Employee(BaseModel):
    nombre: str
    apellidos: str
    telefono: Optional[str] = None

    @pydantic.validator("telefono")
    def phone_validate(cls, value):
        if re.search("^[0-9]{3}(-| )[0-9]{3}(-| )[0-9]{2}(-| )[0-9]{2}$", value) is None:
            raise ValidationError("The phone-number must be like 999-999-99-99")
        return value


class EmployeeAuth(BaseModel):
    employee_id: int
    password: str


class EmployeeRegister(BaseModel):
    name: str
    lastname: str
    phone_number: str
    password: str
    position: str
    store: int

    @pydantic.validator("position")
    def position_validate(cls, value):
        valid_options = ["Manager", "Supervisor", "Inventory Manager", "Cashier"]
        if value not in valid_options:
            raise ValueError(f"Value should be one of {valid_options}")
        return value


class EmployeeUpdate(BaseModel):
    password: str

    @pydantic.validator("password")
    def validate_password(cls, value):
        if len(value)<8:
            raise ValueError("The length of password must be greater than or equal to 8")
        return value
