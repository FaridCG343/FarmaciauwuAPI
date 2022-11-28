from fastapi import APIRouter, HTTPException
from Models.Provider import Provider
from Requests.ProviderRequest import ProviderRequest, ProviderUpdateRequest


provider_routes = APIRouter()


@provider_routes.post("/register")
async def register(new_provider: ProviderRequest):
    Provider.create(
        name=new_provider.name,
        phone_number=new_provider.phoneNumber,
        email=new_provider.email
    )
    return {"message": "The provider has been registered"}


@provider_routes.put("/update")
async def update(provider: ProviderUpdateRequest):
    provider_to_update = Provider.select().where(Provider.id == provider.id).first()
    if provider_to_update:
        if provider.name:
            provider_to_update.name = provider.name
        if provider.email:
            provider_to_update.email = provider.email
        if provider.phoneNumber:
            provider_to_update.phone_number = provider.phoneNumber
        provider_to_update.save()
        return {"message": "The provider has been updated"}
    else:
        return HTTPException(404, "The provider was not found")
