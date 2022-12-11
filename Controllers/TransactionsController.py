from fastapi import APIRouter, Depends, HTTPException
from peewee import fn
from Models.Card import Card
from Models.Transaction import Transaction
from Models.Ticket import Ticket
from Models.Rule import Rule
from Models.AccumulatedProducts import AccumulatedProducts as Ap
from Requests.TransactionRequest import TransactionSaleRequest, TransactionRedeemRequest
from Requests.EmployeeRequest import EmployeeAuth
from fastapi.responses import JSONResponse
from jwtFunctions import verify_cashier_access, verify_credentials
from Models.Stock import Stock
from responseHelper import *


transaction_routes = APIRouter(tags=['Transaction'])


@transaction_routes.post("/quote", dependencies=[Depends(verify_cashier_access)], responses={
    200: set_custom_response("OK",
                             {"card": 1, "products": [{"product_id": 1, "price": 1.0, "units": 1, "subtotal": 10}],
                              "total": 10, "rewards": [{"product_id": 1, "units": 1}]}),
    404: set_404_response()
})
async def quote(request: TransactionSaleRequest):
    if request.card_id:
        card = Card.select().where(Card.id == request.card_id).first()
        if card is None:
            return JSONResponse({"message": "The card was not found"}, 404)
    products = []
    rewards = []
    total = 0

    for product in request.products:
        product_temp = product.dict()
        product_temp['subtotal'] = product.units * product.price
        total += product_temp["subtotal"]
        if request.card_id:
            if get_total_accumulated(product, request.card_id):
                rule, accumulated = get_total_accumulated(product, request.card_id)
                if accumulated // rule.purchaseX > 0:
                    reward = {
                        "product_id": product.product_id,
                        "units": int(accumulated / rule.purchaseX)
                    }
                    rewards.append(reward)
        products.append(product_temp)
    response = {
        "card": request.card_id,
        "products": products,
        "total": total,
        "rewards": rewards
    }
    return JSONResponse(response)


@transaction_routes.post("/sale", responses={
    200: set_custom_response("OK",
                             {"transaction": 1,
                              "card": 1, "products": [{"product_id": 1, "price": 1.0, "units": 1, "subtotal": 10}],
                              "total": 10, "rewards": [{"product_id": 1, "units": 1}]}),
    404: set_404_response()})
async def sale(request: TransactionSaleRequest, employee=Depends(verify_cashier_access)):
    new_transaction = Transaction.create(
        employee_id=employee["employee"]
    )
    if request.card_id:
        card = Card.select().where(Card.id == request.card_id).first()
        if card is None:
            return JSONResponse({"message": "The card was not found"}, 404)
        new_transaction.card_id = request.card_id
    products = []
    rewards = []
    total = 0

    for product in request.products:
        product_temp = product.dict()
        products_avaiable = Stock.select().\
                            where(Stock.product_id == product.product_id).\
                            where(Stock.store_id == employee['store']).first()
        if products_avaiable < product.product_id:
            new_transaction.delete_instance()
            raise HTTPException(400, {"message": 
                "The quantity of products cannot be greater than the quantity available"})
        product_temp['subtotal'] = product.units * product.price
        total += product_temp["subtotal"]
        Ticket.create(
            transaction_id=new_transaction.id,
            product_id=product.product_id,
            subtotal=(product.units * product.price),
            units=product.units,
            store_id=employee["store"]
        )
        if request.card_id:
            if get_total_accumulated(product, request.card_id):
                rule, accumulated = get_total_accumulated(product, request.card_id)
                Ap.create(
                    product_id=product.product_id,
                    card_id=request.card_id,
                    transaction_id=new_transaction.id,
                    units=product.units
                )
                if accumulated//rule.purchaseX > 0:
                    reward = {
                        "product_id": product.product_id,
                        "units": int(accumulated/rule.purchaseX)
                    }
                    rewards.append(reward)
        products.append(product_temp)
    new_transaction.total = total
    new_transaction.save()
    response = {
        "transaction": new_transaction.id,
        "card": request.card_id,
        "products": products,
        "total": total,
        "rewards": rewards
    }
    return JSONResponse(response)


@transaction_routes.post("/redeem", responses={
    200: set_custom_response("OK", {"card": 1, "transaction": 1, "products":
                                    [{"product_id": 1, "price": 1.0, "units": 1, "subtotal": 10}], "total": 0})
})
async def redeem_rewards(request: TransactionRedeemRequest, employee=Depends(verify_cashier_access)):
    response = {'card': request.card_id}
    products = []
    new_transaction = Transaction.create(
        employee_id=employee["employee"],
        total=0,
    )
    card = Card.select().where(Card.id == request.card_id).first()
    if card is None:
        return JSONResponse({"message": "The card was not found"}, 404)
    new_transaction.card_id = request.card_id
    for product in request.rewards:
        if get_total_accumulated(product, card.id):
            rule, total_accumulated = get_total_accumulated(product, card.id)
            total_accumulated -= product.units
            max_pieces_to_redeem = (total_accumulated//rule.purchaseX) * rule.giftY
            if product.units <= max_pieces_to_redeem:
                products.append({**product.dict(), 'subtotal': 0})
                Ticket.create(
                    transaction_id=new_transaction.id,
                    product_id=product.product_id,
                    subtotal=0,
                    units=product.units,
                    store_id=employee["store"]
                )
                negative_accumulation = 0 - (product.units * rule.purchaseX)
                Ap.create(
                    transaction_id=new_transaction.id,
                    product_id=product.product_id,
                    card_id=card.id,
                    units=negative_accumulation
                )
            else:
                new_transaction.delete_instance()
                raise HTTPException(400, {"message": "No claim can be made for excess parts"})
    new_transaction.save()
    response["transaction"] = new_transaction.id
    response['products'] = products
    response['total'] = 0
    return response


@transaction_routes.put("/cancel/{transaction_id}", responses={
    200: set_custom_response("OK", {"message": "The transaction has been canceled"}),
    300: set_custom_response("", {"message": "The credentials belong to an unauthorized person"}),
    400: set_custom_response("Bad request", {"detail": {"message": "Cannot be cancelled because parts have been claimed"
                                                        "with the accumulated proceeds of this transaction."}}),
    401: set_401_response(),

})
async def cancel(transaction_id: int, user=Depends(verify_cashier_access), user_c: EmployeeAuth = None):
    if user['position'] == 'Cashier':
        if user_c.username != "":
            user_a = verify_credentials(user_c)
            if user_a['position'] != 'Manager':
                raise HTTPException(detail={"message": "The credentials belong to an unauthorized person"},
                                    status_code=401)
        else:
            return JSONResponse({"message": "Enter the credentials of someone authorized"}, 300)
    transaction = Transaction.select().where(Transaction.id == transaction_id).first()
    if transaction.status == 'Cancel':
        return JSONResponse({"message": "The transaction is already cancelled"})
    transaction.status = 'Cancel'
    tickets = Ticket.select().where(Ticket.transaction_id == transaction.id).dicts()
    if transaction.card_id:
        for ticket in tickets:
            ap = Ap.select().where(Ap.product_id == int(ticket['product_id'])). \
                where(Ap.transaction_id == transaction.id).first()
            if ap.units > 0:
                results = Ap.select(Ap.product_id, fn.SUM(Ap.units).alias("Cant")). \
                    where(Ap.product_id == int(ticket['product_id'])). \
                    where(Ap.card_id == transaction.card_id). \
                    group_by(Ap.product_id).first()
                if results.Cant - ticket['units'] < 0:
                    raise HTTPException(detail={"message": "Cannot be cancelled because parts have been claimed "
                                                "with the accumulated proceeds of this transaction."},
                                        status_code=400)
    for ticket in tickets:
        stock = Stock.select().where(Stock.product_id == ticket['product_id']).\
            where(Stock.store_id == ticket['store_id']).first()
        stock.available_products += ticket['units']
        stock.save()
        if transaction.card_id:
            ap = Ap.select().where(Ap.product_id == int(ticket['product_id'])).\
                where(Ap.transaction_id == transaction.id).first()
            ap.delete_instance()
    transaction.save()
    return JSONResponse({"message": "The transaction has been canceled"})


@transaction_routes.get("/bonus/list/{card_id}", responses={
    200: set_custom_response("OK", {"card_id": 1, "rewards": [{"product_id": 1, "units": 1}]}),
    404: set_404_response()
})
async def get_bonus_list(card_id: int):
    card = Card.select().where(Card.id == card_id).first()
    if card is None:
        raise HTTPException(404, detail={"message": "Card not found"})
    response = {}
    rewards = []
    products = Ap.select(Ap.product_id, fn.SUM(Ap.units).alias("Cant")).\
        where(Ap.card_id == int(card_id)).\
        group_by(Ap.product_id).dicts()
    for product in products:
        rule = get_rule(product['product_id'])
        if rule:
            accumulated = product['Cant']
            if accumulated // rule.purchaseX > 0:
                reward = {
                    "product_id": product['product_id'],
                    "units": int(accumulated / rule.purchaseX)
                }
                rewards.append(reward)
    response["card_id"] = card_id
    response["rewards"] = rewards
    return JSONResponse(response)


def get_total_accumulated(product, card_id) -> list or None:
    rule = get_rule(product.product_id)
    if rule:
        results = Ap.select(Ap.product_id, fn.SUM(Ap.units).alias("Cant")). \
            where(Ap.product_id == int(product.product_id)). \
            where(Ap.card_id == int(card_id)). \
            group_by(Ap.product_id).dicts()
        total_accumulated = product.units
        if results:
            total_accumulated += results[0]["Cant"]
        return [rule, total_accumulated]
    return None


def get_rule(product_id) -> Rule or None:
    rule = Rule.select(). \
        where(Rule.product_id == product_id). \
        where(Rule.active == 1). \
        where(Rule.type == "Bonus"). \
        first()
    if rule:
        return rule
    return None
