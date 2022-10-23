from fastapi import *
from Models.Databases import maria
from Controllers import ClientController as Cc

uwuAPI = FastAPI(title="FarmaciauwuAPI", description="API para mi POS", version="1.0.0")


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


@uwuAPI.post("/client/affiliate")
async def create_client(client):
    Cc.client_create(client)


@uwuAPI.get("/client/{client_id}")
async def get_client(client_id):
    return Cc.get_client(client_id)
