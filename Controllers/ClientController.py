from os import getenv

from Models.Client import Client
from Models.Card import Card
from Requests.ClienteRequest import ClienteRequest
from Requests.ClienteRequest import ClientUpdateRequest
from fastapi import APIRouter
from datetime import date
from fastapi.responses import JSONResponse


cliente_routes = APIRouter()


@cliente_routes.post("/affiliate")
async def client_create(c: ClienteRequest):
    client = Client.select().where(Client.phoneNumber == c.telefono or Client.email == c.correo).first()
    if client:
        return JSONResponse({"message": "There's already an existing record"}, status_code=405)
    new_client = Client.create(
        name=c.nombre,
        lastname=c.apellidos,
        phoneNumber=c.telefono,
        email=c.correo,
        address=c.direccion
    )
    # new_client.save()
    num_cliente = new_client.getinfo()["id"]
    card = Card.create(
        client_id=num_cliente,
        register_date=date.today()
    )
    # card.save()
    response = JSONResponse({
        "numTarjeta": card.getinfo()["id"],
        "numCliente": num_cliente
    })
    return response


@cliente_routes.get("/{client_id}")
async def get_client(client_id):
    print(getenv("HOST"))
    client = Client.select().where(Client.id == client_id).first()
    if client:
        card = Card.select().where(Card.client_id == client.getinfo()["id"]).first()
        r = JSONResponse({**client.getinfo(), "card_id": card.getinfo()["id"]})
        return r
    else:
        return JSONResponse({"message": "Client not found"}, 404)


@cliente_routes.put("/update/{client_id}")
async def update_client(client_id, c: ClientUpdateRequest):
    client = Client.select().where(Client.id == client_id).first()
    if c.correo is not None:
        client.email = c.correo
    if c.nombre is not None:
        client.name = c.nombre
    if c.apellidos is not None:
        client.lastname = c.apellidos
    if c.telefono is not None:
        client.phoneNumber = c.telefono
    if c.direccion is not None:
        client.address = c.direccion
    if c.correo is None and c.telefono is None and c.nombre is None and c.apellidos is None and c.direccion is None:
        return JSONResponse({"message": "The request is empty"}, 401)
    client.save()
    return JSONResponse({"message": "Update successfully"})

