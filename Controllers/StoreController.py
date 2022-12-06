from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from Models.Store import Store
from Requests.StoreRequest import StoreRequest, StoreUpdateRequest
from responseHelper import *


store_routes = APIRouter(tags=['Store'])


@store_routes.get("/{name}", responses={
    200: set_custom_response("OK", {
      "name": "Durango",
      "address": "Henequén 1651, Prados de Salvarcar",
      "active": True
    }),
    404: set_404_response()
})
async def get_store(name: str):
    store = Store.select().where((Store.name == name) & (Store.active == 1)).first()
    if store:
        return JSONResponse(store.todict())
    else:
        raise HTTPException(404, detail={"message", "Store not found or not active"})


@store_routes.post("/register", responses={
    200: set_custom_response("OK", {"message": "The store has been created successfully"}),
    409: set_409_response()
})
async def register(new_store: StoreRequest):
    store = Store.select().where((Store.name == new_store.name)).first()
    if store:
        raise HTTPException(409, detail={"message": "There's already and existing record"})
    Store.create(
        name=new_store.name,
        address=new_store.address,
        active=new_store.active
    )
    return {"message": "The store has been created successfully"}


@store_routes.put("/update", responses={
    200: set_custom_response("OK", {"message": "The store has been updated"}),
    404: set_404_response()
})
async def update(store: StoreUpdateRequest):
    store_to_update = Store.select().where(Store.id == store.id).first()
    if store_to_update:
        if store.name:
            store_to_update.name = store.name
        if store.active:
            store_to_update.active = store.active
        store_to_update.save()
        return {"message": "The store has been updated"}
    else:
        raise HTTPException(404, {"message": "The store was not found"})
