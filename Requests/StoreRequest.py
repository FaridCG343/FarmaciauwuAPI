from pydantic import BaseModel
from pydantic.typing import Optional


class StoreRequest(BaseModel):
    name: str
    address: str
    active: Optional[bool] = True


class StoreUpdateRequest(BaseModel):
    id: int
    name: Optional[str] = None
    active: Optional[bool] = None
