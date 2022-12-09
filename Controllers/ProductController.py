import peewee
from fastapi import APIRouter, HTTPException, Depends
from Models.Product import Product
from Models.Rule import Rule
from fastapi.responses import JSONResponse
from responseHelper import *
from jwtFunctions import verify_inventory_manager_access, verify_manager_access
from Requests.ProductRequest import ProductRequest, ProductUpdate


product_routes = APIRouter(tags=['Product'])


@product_routes.get("/list")
async def get_list_products():
    # products = [product for product in Product.select().dicts()]
    products = Product.select().dicts()
    l_products = []
    for product in products:
        rule = Rule.select().where(Rule.product_id == product['id']).where(Rule.active == 1).first()
        product["originalPrice"] = product["price"]
        if rule:
            if rule.type == "Discount":
                product["price"] = round(product["price"] * (1 - rule.discount), 2)
            product[rule.type] = rule.description
        l_products.append(product)
    return l_products


@product_routes.get("/{product_id}", responses={
    200: set_custom_response("OK", {
      "id": 1,
      "name": "Paracetamol",
      "description": "Paracetamol 500 mg oral 20 tabletas",
      "price": 28,
      "originalPrice": 28,
      "Bonus[if applicable]": "Compra 2 paracetamol 20 tabletas y llevate 1 de regalo"
    }),
    404: set_404_response()
})
async def get_product(product_id: int):
    product = Product.select().where(Product.id == product_id).dicts()
    if product:
        rule = Rule.select().where(Rule.product_id == product_id).where(Rule.active == 1).first()
        product[0]["originalPrice"] = product[0]["price"]
        if rule:
            if rule.type == "Discount":
                product[0]["price"] = round(product[0]["price"]*(1-rule.discount), 2)

            return JSONResponse(content={**product[0], rule.type: rule.description})
        return product[0]
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@product_routes.get("/search/{name}", responses={
    200: set_custom_response("OK", [
      {
        "id": 2,
        "name": "Naproxeno",
        "description": "Naproxeno 500 mg oral 20 tabletas",
        "price": 53,
        "originalPrice": 53,
        "Bonus": "Compra 3 naproxeno y llevate 1 de regalo"
      }]),
    404: set_404_response()
    })
async def get_product_by_name(name: str):
    product = Product.select().\
        where(Product.name.contains(name)).\
        dicts()
    if product:
        response = []
        for p in product:
            rule = Rule.select().where(Rule.product_id == p["id"]).where(Rule.active == 1).first()
            p["originalPrice"] = p["price"]
            if rule:
                if rule.type == "Discount":
                    p["price"] = round(p["price"]*(1-rule.discount), 2)
                p[rule.type] = rule.description
            response.append(p)
        return JSONResponse(response)
    raise HTTPException(404, "Product not found")


@product_routes.post("/register", dependencies=[Depends(verify_manager_access)], responses={
    200: set_custom_response("OK", {"message": "Product registered successfully"}),
    409: set_409_response()
})
async def register_product(product: ProductRequest):
    existing_product = Product.select().where(
        (Product.name == product.name) & (Product.description == product.description))
    if existing_product:
        raise HTTPException(409, detail={"detail": {"message": "There's already an existing record"}})
    new_product = Product.create(
        name=product.name,
        description=product.description,
        price=product.price
    )
    return JSONResponse({"message": "Product registered successfully", **new_product.todict()})


@product_routes.put("/update/{product_id}", responses={
    200: set_custom_response("OK", {"message": "Product updated successfully"}),
    400: set_custom_response("Bad request", {"detail": {"message": "The request is empy"}}),
    404: set_404_response(),
    409: set_409_response()
}, dependencies=[Depends(verify_inventory_manager_access)])
async def update_product(product_id: int, product: ProductUpdate):
    product_to_update = Product.select().where(Product.id == product_id).first()
    if product_to_update is None:
        raise HTTPException(404, detail={"message": "Product not found"})
    if product.name != '':
        product_to_update.name = product.name
    if product.description != '':
        product_to_update.description = product.description
    if product.price is not None:
        product_to_update.price = product.price
    if product.name == '' and product.description == '' and product.price is None:
        raise HTTPException(400, detail={"message": "The request is empty"})
    try:
        product_to_update.save()
    except peewee.IntegrityError as e:
        raise HTTPException(409, detail={"message": "There's already an existing record"})
    return JSONResponse({"message": "Product updated successfully"})


@product_routes.delete("/delete/{product_id}")
async def delete_product_by_id(product_id: int):
    print(product_id)
    product = Product.select().where(Product.id == product_id).first()
    print(product.name)
    if product is None:
        raise HTTPException(404, {"message": "Product not found"})
    product.delete_instance()
    return JSONResponse({"message": "product delete successfully"})
