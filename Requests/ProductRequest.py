from pydantic.types import NegativeInt
from pydantic.typing import Optional
from pydantic import BaseModel, validator, conint
from fastapi import HTTPException


class ProductTicket(BaseModel):
    product_id: int
    price: float
    units: conint(gt=0)
    bonus_units: Optional[conint(lt=1)] = 0
    subtotal: float


class ProductReward(BaseModel):
    product_id: int
    units: int


