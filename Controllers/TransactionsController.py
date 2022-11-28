from fastapi import APIRouter, Depends, HTTPException
from peewee import fn
from Models.Card import Card
from Models.Transaction import Transaction
from Models.Ticket import Ticket
from Models.Rule import Rule
from Models.AccumulatedProducts import AccumulatedProducts as Ap
from Requests.TransactionRequest import TransactionSaleRequest, TransactionRedeemRequest
from fastapi.responses import JSONResponse
from jwtFunctions import verify_cashier_access

transaction_routes = APIRouter()


@transaction_routes.post("/sale")
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
        "card": request.card_id,
        "products": products,
        "total": total,
        "rewards": rewards
    }
    return JSONResponse(response)


@transaction_routes.post("/redeem")
async def redeem_rewards(request: TransactionRedeemRequest, employee=Depends(verify_cashier_access)):
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
            max_pieces_to_redeem = (total_accumulated//rule.purchaseX) * rule.giftY
            if max_pieces_to_redeem <= product.units:
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
                    units = negative_accumulation
                )
            else:
                raise HTTPException(400, {"message", ""})
    new_transaction.save()


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
