import pydantic
from pydantic import BaseModel, validator
from fastapi import HTTPException


class ProductTicket(BaseModel):
    product_id: int
    price: float
    units: int
    subtotal: float

    @pydantic.validator("units")
    @classmethod
    def quantity_validate(cls, value):
        if value <= 0:
            raise HTTPException(400, "The units can't be less than 1")
        return value


class ProductReward(BaseModel):
    product_id: int
    units: int


