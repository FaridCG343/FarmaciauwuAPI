from fastapi import FastAPI, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from Models import Databases
from Controllers.EmployeeController import employee_routes
from dotenv import load_dotenv
from Controllers.ClientController import cliente_routes
from Controllers.TransactionsController import transaction_routes
from Controllers.ProductController import product_routes
from Controllers.StoreController import store_routes
from Controllers.ProviderController import provider_routes
from Controllers.StockController import stock_routes
from Requests.EmployeeRequest import EmployeeAuth
from jwtFunctions import verify_cashier_access, verify_inventory_manager_access, verify_credentials, write_token
from responseHelper import *

uwuAPI = FastAPI(title="FarmaciauwuAPI", description="API para mi POS", version="2.0.0")
uwuAPI.include_router(employee_routes, prefix="/employee")
uwuAPI.include_router(cliente_routes, prefix="/client", dependencies=[Depends(verify_cashier_access)])
uwuAPI.include_router(transaction_routes, prefix="/transaction")
uwuAPI.include_router(product_routes, prefix="/product")
uwuAPI.include_router(store_routes, prefix="/store")
uwuAPI.include_router(provider_routes, prefix="/provider", dependencies=[Depends(verify_inventory_manager_access)])
uwuAPI.include_router(stock_routes, prefix="/stock")

uwuAPI.add_middleware(CORSMiddleware, allow_origins=['*'],
                      allow_credentials=True,
                      allow_methods=["*"],
                      allow_headers=["*"], )


@uwuAPI.on_event("startup")
def startup():
    if Databases.maria.is_closed():
        Databases.maria.connect()


@uwuAPI.on_event("shutdown")
def shutdown():
    if not Databases.maria.is_closed():
        Databases.maria.close()


@uwuAPI.post("/login", responses={
    200: set_custom_response("OK", {"message": "Login successful", "token": "token_uwu"}),
    400: set_custom_response("Bad request", {"detail": {"message": "Incorrect password"}}),
    404: set_404_response()
}, tags=["Login"])
async def login(user: EmployeeAuth, response: Response):
    info, pos = verify_credentials(user, True)
    token = write_token(info)
    response.set_cookie(key="token_c", value=token, httponly=True)
    return {"message": "Login successful", "token": token, "position": pos}


@uwuAPI.post("/logout", tags=["Logout"])
async def logout(response: Response):
    response.delete_cookie(key="token")
    return {"message": "Logout successful"}


load_dotenv()
