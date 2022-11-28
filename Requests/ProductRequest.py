from pydantic import BaseModel, validator, conint


class ProductTicket(BaseModel):
    product_id: int
    price: float
    units: conint(gt=0)


class ProductReward(BaseModel):
    product_id: int
    units: int


