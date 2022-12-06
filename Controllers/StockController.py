from fastapi import APIRouter, Depends, HTTPException
from jwtFunctions import verify_inventory_manager_access
from Requests.StockRequest import StockRequest, StockDepletionRequest
from Models.Stock import Stock
from Models.StockLogs import StockLogs
from responseHelper import *


stock_routes = APIRouter(tags=["Stock"])


@stock_routes.put('/add', responses={
    200: set_custom_response("OK", {"message": "Products added successfully"}),
    401: set_401_response()
})
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


@stock_routes.put("/depletion", responses={
    200: set_custom_response("OK", {"message": "Successful"}),
    400: set_custom_response(
        "Bad request",
        {"detail": {"message": "The amount of shrinkage cannot be greater than the products available"}}),
    401: set_401_response()
})
async def depletion(request: StockDepletionRequest, user_info=Depends(verify_inventory_manager_access)):
    stock = Stock.select(). \
        where(Stock.product_id == request.product). \
        where(Stock.store_id == user_info["store"]). \
        first()
    stock.available_products -= request.cant
    if stock.available_products - request.cant < 0:
        raise HTTPException(400,
                            detail={"message": "The amount of shrinkage cannot be greater than the products available"})
    stock.save()
    StockLogs.create(
        store_id=user_info["store"],
        product_id=request.product,
        quantity=request.cant
    )
    return {"message": "Successful"}
