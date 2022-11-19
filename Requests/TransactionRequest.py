import pydantic
from pydantic import BaseModel
from Requests.ProductRequest import ProductTicket
from pydantic.typing import Optional
from typing import List


class TransactionRequest(BaseModel):
    employee_id: int
    total: float
    card_id: Optional[int] = None
    products: List[ProductTicket]
    choosedGift: Optional[bool] = False

