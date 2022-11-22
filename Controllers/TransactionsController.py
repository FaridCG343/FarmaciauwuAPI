from fastapi import APIRouter, HTTPException
from peewee import fn
from Models.Card import Card
from Models.Transaction import Transaction
from Models.Ticket import Ticket
from Models.Rule import Rule
from Models.AccumulatedProducts import AccumulatedProducts as Ap
from Requests.TransactionRequest import TransactionRequest, TransactionSaleRequest, TransactionRedeemRequest
from fastapi.responses import JSONResponse
from datetime import date

transaction_routes = APIRouter()


@transaction_routes.post("/get_rewards")
async def get_rewards(request: TransactionRequest):
    rewards = []
    for product in request.products:
        if get_total_accumulated(product, request.card_id):
            rule, total_accumulated = get_total_accumulated(product, request.card_id)
            if total_accumulated >= rule.purchaseX:
                rewards.append({"product_id": product.product_id,
                                "units": int((total_accumulated * rule.giftY) // rule.purchaseX)})
    response = request.dict()
    response["rewards"] = rewards
    return response


@transaction_routes.post("/sale")
async def sale(request: TransactionSaleRequest):
    if request.card_id:
        card = Card.select().where(Card.id == request.card_id).first()
        if card is None:
            return JSONResponse({"message": "The card number was not found"}, status_code=404)
    new_transaction = Transaction.create(
        employee_id=request.employee_id,
        date=date.today(),
        card_id=request.card_id,
        total=request.total
    )
    transaction_id = new_transaction.id
    new_total = 0
    for product in request.products:
        Ticket.create(
            transaction_id=transaction_id,
            product_id=product.product_id,
            subtotal=product.subtotal,
            quantity=product.units
        )
        new_total += product.subtotal
        if request.card_id:
            rule = get_rule(product.product_id)
            if rule:
                Ap.create(
                    product_id=product.product_id,
                    card_id=request.card_id,
                    transaction_id=transaction_id,
                    units=product.units
                )
                if product.bonus_units < 0:
                    Ap.create(
                        product_id=product.product_id,
                        card_id=request.card_id,
                        transaction_id=transaction_id,
                        units=product.bonus_units
                    )
                    Ap.create(
                        product_id=product.product_id,
                        card_id=request.card_id,
                        transaction_id=transaction_id,
                        units=product.bonus_units * rule.purchaseX
                    )
    new_transaction.total = new_total
    new_transaction.save()
    response = {
        "message": "Your purchase has been registered",
        "details": request.products,
        "total": new_total,
        "transaction_number": transaction_id
    }
    return response


@transaction_routes.post("/redeem")
async def redeem_rewards(request: TransactionRedeemRequest):
    response = {}
    card = Card.select().where(Card.id == request.card_id).first()
    if card is None:
        return JSONResponse({"message": "The card number was not found"}, status_code=404)
    reward_units = {}
    for reward in request.rewards:
        reward_units[reward.product_id] = reward.units

    new_products = []
    for product in request.products:
        if get_total_accumulated(product, request.card_id):
            rule, total_accumulated = get_total_accumulated(product, request.card_id)
            if rule and product.product_id in reward_units.keys():
                if (total_accumulated - (reward_units[product.product_id] * rule.purchaseX)) < 0:
                    raise HTTPException(406, "The reward units to claim is greater than ")
                    # Add to message "lo que corresponde"
                if (total_accumulated - (reward_units[product.product_id] * rule.purchaseX)) == 0:
                    product.units += reward_units[product.product_id]
                    product.bonus_units -= reward_units[product.product_id]
                if (total_accumulated - (reward_units[product.product_id] * rule.purchaseX)) > 0:
                    units_to_add = abs(reward_units[product.product_id] - product.units)
                    product.units += units_to_add
                    product.bonus_units -= reward_units[product.product_id]
        new_products.append(product)
    response["card_id"] = request.card_id
    response["products"] = new_products
    return response


def get_total_accumulated(product, card_id) -> list or None:
    rule = get_rule(product.product_id)
    if rule:
        results = Ap.select(Ap.product_id, fn.SUM(Ap.units).alias("Cant")). \
            where(Ap.product_id == int(product.product_id)). \
            where(Ap.card_id == int(card_id)). \
            group_by(Ap.product_id).dicts()
        total_accumulated = (product.units + product.bonus_units) + (product.bonus_units * rule.purchaseX)
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
