from pydantic import BaseModel
from pydantic.typing import Optional
import pydantic


class ProductTicket(BaseModel):
    product_id: int
    price: float
    quantity: int
    subtotal: float


class Product(BaseModel):
    product_id: int
