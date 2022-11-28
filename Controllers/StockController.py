from fastapi import APIRouter, Depends
from jwtFunctions import verify_inventory_manager_access
from Requests.StockRequest import StockRequest, StockDepletionRequest
from Models.Stock import Stock
from Models.StockLogs import StockLogs


stock_routes = APIRouter()


@stock_routes.put('/add')
async def add_to_stock(request: StockRequest, user_info=Depends(verify_inventory_manager_access)):
    stock = Stock.select().\
        where(Stock.product_id == request.product).\
        where(Stock.store_id == user_info["store"]).\
        first()
    if stock is None:
        stock = Stock.create(
            store_id=user_info["store"],
            product_id=request.product,
            available_product=0
        )
    stock.available_products += request.cant
    stock.save()
    StockLogs.create(
        provider_id=request.provider,
        store_id=user_info["store"],
        product_id=request.product,
        quantity=request.cant
    )
    return {"message": "Products added successfully"}


@stock_routes.put("/depletion")
async def depletion(request: StockDepletionRequest, user_info=Depends(verify_inventory_manager_access)):
    stock = Stock.select(). \
        where(Stock.product_id == request.product). \
        where(Stock.store_id == user_info["store"]). \
        first()
    if stock is None:
        stock = Stock.create(
            store_id=user_info["store"],
            product_id=request.product,
            available_product=0
        )
    stock.available_products += request.cant
    stock.save()
    StockLogs.create(
        store_id=user_info["store"],
        product_id=request.product,
        quantity=request.cant
    )
    return {"message": "Products added successfully"}