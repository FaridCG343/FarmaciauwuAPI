from fastapi import FastAPI
from Models import Databases
from Controllers.EmployeeController import employee_routes
from dotenv import load_dotenv
from Controllers.ClientController import cliente_routes
from Controllers.TransactionsController import transaction_routes


uwuAPI = FastAPI(title="FarmaciauwuAPI", description="API para mi POS", version="1.0.0")
uwuAPI.include_router(employee_routes, prefix="/employee")
uwuAPI.include_router(cliente_routes, prefix="/client")
uwuAPI.include_router(transaction_routes, prefix="/transaction")


@uwuAPI.on_event("startup")
def startup():
    if Databases.maria.is_closed():
        Databases.maria.connect()


@uwuAPI.on_event("shutdown")
def shutdown():
    if not Databases.maria.is_closed():
        Databases.maria.close()


@uwuAPI.get("/")
async def index():
    return "Bienvenido"


load_dotenv()
