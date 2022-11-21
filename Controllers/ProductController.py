from fastapi import APIRouter, HTTPException
from Models.Product import Product
from Models.Rule import Rule
from fastapi.responses import JSONResponse
from peewee import Expression


product_routes = APIRouter()


@product_routes.get("/{product_id}")
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


@product_routes.get("/search/{name}")
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
        return response
    raise HTTPException(404, "Product not found")


