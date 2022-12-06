from Models.Client import Client
from Models.Card import Card
from Requests.ClienteRequest import ClienteRequest
from Requests.ClienteRequest import ClientUpdateRequest
from fastapi import APIRouter, HTTPException
from datetime import date
from fastapi.responses import JSONResponse
from responseHelper import *


cliente_routes = APIRouter(tags=["Client"])


@cliente_routes.post("/affiliate", responses={
    200: set_custom_response("OK", {"message": "Client registered successfully", "numTarjeta": 1, "numCliente": 1}),
    401: set_401_response(),
    409: set_409_response()
})
async def client_create(c: ClienteRequest):
    client = Client.select().where((Client.phoneNumber == c.telefono) | (Client.email == c.correo)).first()
    if client:
        raise HTTPException(detail={"message": "There's already an existing record"}, status_code=409)
    new_client = Client.create(
        name=c.nombre,
        lastname=c.apellidos,
        phoneNumber=c.telefono,
        email=c.correo,
        address=c.direccion
    )
    num_cliente = new_client.id
    card = Card.create(
        client_id=num_cliente,
        register_date=date.today()
    )
    response = JSONResponse({
        "message": "Client registered successfully",
        "numTarjeta": card.id,
        "numCliente": num_cliente
    })
    return response


@cliente_routes.get("/{client_id}", responses={
    200: set_custom_response("OK", {
      "name": "farid",
      "lastname": "castillo",
      "phoneNumber": "123-456-78-90",
      "address": "address",
      "email": "example@gmail.com",
      "card_id": 1
    }),
    401: set_401_response(),
    404: set_404_response()
})
async def get_client(client_id: int):
    client = Client.select().where(Client.id == client_id).first()
    if client:
        card = Card.select().where(Card.client_id == client.id).first()
        r = JSONResponse({**client.todict(), "card_id": card.id})
        return r
    else:
        raise HTTPException(detail={"message": "Client not found"}, status_code=404)


@cliente_routes.put("/update/{client_id}", responses={
    200: set_custom_response("OK", {"message": "Update successfully"}),
    400: set_custom_response("Bad request", {"detail": {"message": "The request is empty"}}),
    401: set_401_response(),
    404: set_404_response(),
    409: set_409_response()
})
async def update_client(client_id, c: ClientUpdateRequest):
    client = Client.select().where(Client.id == client_id).first()
    if client is None:
        raise HTTPException(404, detail={"detail": {"message": "Client not found"}})
    existing_data = Client.select().where((Client.email == c.correo) | (Client.phoneNumber == c.telefono)).first()
    if existing_data:
        raise HTTPException(409, detail={"detail": {"message": "There's already an existing record"}})
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
        raise HTTPException(detail={"message": "The request is empty"}, status_code=400)
    client.save()
    return JSONResponse({"message": "Update successfully"})
