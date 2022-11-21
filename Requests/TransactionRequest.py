import pydantic
from pydantic import BaseModel
from Requests.ProductRequest import ProductTicket, ProductReward
from pydantic.typing import Optional
from typing import List


class TransactionRequest(BaseModel):
    card_id: int
    products: List[ProductTicket]


class TransactionSaleRequest(BaseModel):
    employee_id: int
    total: float
    card_id: Optional[int] = None
    products: List[ProductTicket]
    rewards: Optional[List[ProductReward]] = None


class TransactionRedeemRequest(BaseModel):
    card_id: int
    products: List[ProductTicket]
    rewards: List[ProductReward]
