import peewee
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from Models.Provider import Provider
from Requests.ProviderRequest import ProviderRequest, ProviderUpdateRequest
from responseHelper import *


provider_routes = APIRouter(tags=["Provider"])


@provider_routes.get("/{name}", responses={
    200: set_custom_response("OK", [
      {
        "id": 1,
        "name": "Farma-Medical",
        "phone_number": "656-616-07-81",
        "email": "famamedical@gmail.com"
      }
    ]),
    401: set_401_response(),
    404: set_404_response()
})
async def get_provider(name: str):
    providers = Provider.select(). \
        where(Provider.name.contains(name)).dicts()
    if providers:
        return JSONResponse(list(providers))
    else:
        raise HTTPException(404, detail={"message": "Provider not found"})


@provider_routes.post("/register", responses={
    200: set_custom_response("OK", {"message": "The provider has been registered"}),
    401: set_401_response(),
    409: set_409_response()
})
async def register(new_provider: ProviderRequest):
    existing_provider = Provider.select().where(
        (Provider.email == new_provider.email) | (Provider.phone_number == new_provider.phoneNumber)
        | (Provider.name == new_provider.name)
    ).first()
    if existing_provider:
        raise HTTPException(409, detail={"message": "There's already an existing record"})
    Provider.create(
        name=new_provider.name,
        phone_number=new_provider.phoneNumber,
        email=new_provider.email
    )
    return {"message": "The provider has been registered"}


@provider_routes.put("/update/{name}", responses={
    200: set_custom_response("OK", {"message": "The provider has been updated"}),
    401: set_401_response(),
    404: set_404_response(),
    409: set_409_response()
})
async def update(name: str, provider: ProviderUpdateRequest):
    provider_to_update = Provider.select().where(Provider.name == name).first()
    if provider_to_update:
        if provider.name:
            provider_to_update.name = provider.name
        if provider.email:
            provider_to_update.email = provider.email
        if provider.phoneNumber:
            provider_to_update.phone_number = provider.phoneNumber
        try:
            provider_to_update.save()
        except peewee.IntegrityError as e:
            raise HTTPException(409, detail={"message": "There's already an existing record"})
        return {"message": "The provider has been updated"}
    else:
        return HTTPException(404, "The provider was not found")
