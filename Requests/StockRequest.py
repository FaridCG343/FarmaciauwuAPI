from pydantic import BaseModel, conint


class StockRequest(BaseModel):
    provider: int
    product: int
    cant: conint(gt=0)


class StockDepletionRequest(BaseModel):
    product: int
    cant: conint(lt=0)
