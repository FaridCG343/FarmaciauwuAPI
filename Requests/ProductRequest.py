from pydantic import BaseModel, conint
from pydantic.typing import Optional


class ProductRequest(BaseModel):
    name: str
    description: str
    price: float


class ProductUpdate(BaseModel):
    name: Optional[str] = ''
    description: Optional[str] = ''
    price: Optional[float] = None


class ProductTicket(BaseModel):
    product_id: int
    price: float
    units: conint(gt=0)


class ProductReward(BaseModel):
    product_id: int
    units: int


