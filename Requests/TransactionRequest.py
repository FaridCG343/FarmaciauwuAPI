from pydantic import BaseModel
from Requests.ProductRequest import ProductTicket, ProductReward
from pydantic.typing import Optional
from typing import List


class Payment(BaseModel):
    type: str
    currency: str


class TransactionQuoteRequest(BaseModel):
    card_id: Optional[int]
    products: List[ProductTicket]


class TransactionSaleRequest(BaseModel):
    card_id: Optional[int] = None
    products: List[ProductTicket]


class TransactionRedeemRequest(BaseModel):
    card_id: int
    rewards: List[ProductReward]
