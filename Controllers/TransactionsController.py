from fastapi import APIRouter, HTTPException
from peewee import fn
from Models.Card import Card
from Models.Transaction import Transaction
from Models.Ticket import Ticket
from Models.Rule import Rule
from Models.AccumulatedProducts import AccumulatedProducts as Ap
from Requests.TransactionRequest import TransactionQuoteRequest, TransactionSaleRequest, TransactionRedeemRequest
from fastapi.responses import JSONResponse
from datetime import date

transaction_routes = APIRouter()


@transaction_routes.post("/quote")
async def quote(request: TransactionQuoteRequest):
    pass


@transaction_routes.post("/sale")
async def sale(request: TransactionSaleRequest):
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
                if accumulated/rule.purchaseX > 0:
                    reward = {
                        "product_id": product.product_id,
                        "units": int(round(accumulated/rule.purchaseX))
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


@transaction_routes.post("/redeem")
async def redeem_rewards(request: TransactionRedeemRequest):
    pass


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
