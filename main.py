from fastapi import FastAPI
from Models.Databases import maria
from Controllers.EmployeeController import employee_routes
from dotenv import load_dotenv
from Controllers.ClientController import cliente_routes


uwuAPI = FastAPI(title="FarmaciauwuAPI", description="API para mi POS", version="1.0.0")
uwuAPI.include_router(employee_routes, prefix="/employee")
uwuAPI.include_router(cliente_routes, prefix="/client")


@uwuAPI.on_event("startup")
def startup():
    if maria.is_closed():
        maria.connect()


@uwuAPI.on_event("shutdown")
def shutdown():
    if not maria.is_closed():
        maria.close()


@uwuAPI.get("/")
async def index():
    return "Bienvenido"


load_dotenv()
