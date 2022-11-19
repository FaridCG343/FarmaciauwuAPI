import pydantic
from pydantic import BaseModel, validator
from fastapi import HTTPException


class ProductTicket(BaseModel):
    product_id: int
    price: float
    quantity: int
    subtotal: float

    @pydantic.validator("quantity")
    @classmethod
    def quantity_validate(cls, value):
        if value <= 0:
            raise HTTPException(400, "The quantity can't be less than 1")
        return value


class Product(BaseModel):
    product_id: int
