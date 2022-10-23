from Models.Client import Client
from Requests import ClienteRequest
from fastapi import HTTPException


def client_create(client: ClienteRequest):
    new_client = Client.create(
        nombre=client.nombre,
        apellidos=client.apellidos,
        telefono=client.telefono,
        correo=client.correo,
        direccion=client.direccion
    )
    new_client.save()
    return new_client.getInfo()["id"]


def get_client(client_id):
    client = Client.select().where(Client.id_cliente == client_id).first()
    if client:
        return client
    else:
        raise HTTPException(404, "Client not found")
