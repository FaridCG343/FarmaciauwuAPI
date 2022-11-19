from fastapi import APIRouter
from peewee import fn
from Models.Card import Card
from Models.Transaction import Transaction
from Models.Ticket import Ticket
from Models.Rule import Rule
from Models.AccumulatedProducts import AccumulatedProducts as Ap
from Requests.TransactionRequest import TransactionRequest
from fastapi.responses import JSONResponse
from datetime import date

transaction_routes = APIRouter()


@transaction_routes.post("/redeem")
async def redeem():
    pass


@transaction_routes.post("/sale")
async def sale(request: TransactionRequest):
    if request.card_id is None:
        # Falta registrar la venta pero sin tarjeta
        return JSONResponse({"message": "Your purchase has been registered"}, status_code=200)
    card = Card.select().where(Card.id == request.card_id).first()
    if card is None:
        return JSONResponse({"message": "The card number was not found"}, status_code=404)
    rewards = []
    new_transaction = Transaction.create(
        employee_id=request.employee_id,
        card_id=request.card_id,
        date=date.today(),
        total=request.total
    )
    new_transaction.save()
    transaction_id = new_transaction.id
    for product in request.products:
        rule = Rule.select(). \
            where(Rule.product_id == product.product_id). \
            where(Rule.active == 1). \
            where(Rule.type == "Bonus"). \
            first()
        ticket_temp = Ticket.create(
            transaction_id=transaction_id,
            product_id=product.product_id,
            subtotal=product.subtotal,
            quantity=product.quantity
        )

        if rule:
            results = Ap.select(Ap.product_id, fn.SUM(Ap.units).alias("Cant")). \
                where(Ap.product_id == int(product.product_id)). \
                where(Ap.card_id == int(request.card_id)). \
                group_by(Ap.product_id).dicts()
            total_accumulated = product.quantity
            if results:
                total_accumulated += results[0]["Cant"]
            if total_accumulated >= rule.purchaseX:
                rewards.append({"product_id": product.product_id,
                                "quantityBonus": int((total_accumulated * rule.giftY) // rule.purchaseX)})
            accumulated = Ap.create(
                product_id=product.product_id,
                card_id=request.card_id,
                transaction_id=transaction_id,
                units=product.quantity
            )
    response = {
        "message": "Your purchase has been registered",
        "details": request.products,
        "total": request.total
    }
    if rewards:
        response["rewards"] = rewards
    return response
