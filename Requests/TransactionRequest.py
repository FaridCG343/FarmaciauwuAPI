import pydantic
from pydantic import BaseModel
from Requests.ProductRequest import ProductTicket, ProductReward
from pydantic.typing import Optional
from enum import Enum
from typing import List


class Payment(BaseModel):
    type: str
    currency: str


class TransactionQuoteRequest(BaseModel):
    card_id: Optional[int]
    products: List[ProductTicket]


class TransactionSaleRequest(BaseModel):
    employee_id: int
    card_id: Optional[int] = None
    products: List[ProductTicket]
    payments: List[Payment]


class TransactionRedeemRequest(BaseModel):
    card_id: int
    rewards: List[ProductReward]
