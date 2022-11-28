from fastapi import APIRouter, HTTPException
from Models.Store import Store
from Requests.StoreRequest import StoreRequest, StoreUpdateRequest


store_routes = APIRouter()


@store_routes.post("/register")
async def register(new_store: StoreRequest):
    Store.create(
        name=new_store.name,
        address=new_store.address,
        active=new_store.active
    )
    return {"message": "The store has been created successfully"}


@store_routes.put("/update")
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
