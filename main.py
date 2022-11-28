from fastapi import FastAPI, Depends
from Models import Databases
from Controllers.EmployeeController import employee_routes
from dotenv import load_dotenv
from Controllers.ClientController import cliente_routes
from Controllers.TransactionsController import transaction_routes
from Controllers.ProductController import product_routes
from Controllers.StoreController import store_routes
from Controllers.ProviderController import provider_routes
from Controllers.StockController import stock_routes
# from jwtFunctions import verify_manager_access


uwuAPI = FastAPI(title="FarmaciauwuAPI", description="API para mi POS", version="2.0.0")
uwuAPI.include_router(employee_routes, prefix="/employee")
uwuAPI.include_router(cliente_routes, prefix="/client")
uwuAPI.include_router(transaction_routes, prefix="/transaction")
uwuAPI.include_router(product_routes, prefix="/product")
uwuAPI.include_router(store_routes, prefix="/store")
uwuAPI.include_router(provider_routes, prefix="/provider")
uwuAPI.include_router(stock_routes, prefix="/stock")


@uwuAPI.on_event("startup")
def startup():
    if Databases.maria.is_closed():
        Databases.maria.connect()


@uwuAPI.on_event("shutdown")
def shutdown():
    if not Databases.maria.is_closed():
        Databases.maria.close()


load_dotenv()
