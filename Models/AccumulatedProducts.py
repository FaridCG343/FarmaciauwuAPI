from peewee import *
from Models.Databases import maria
from Models.Product import Product
from Models.Card import Card
from Models.Transaction import Transaction


class AccumulatedProducts(Model):
    product_id = ForeignKeyField(Product)
    card_id = ForeignKeyField(Card)
    transaction_id = ForeignKeyField(Transaction)
    units = IntegerField()

    class Meta:
        database = maria
        table_name = "accumulated_products"

    def getinfo(self) -> dict:
        c: dict = {
            "producto": self.product_id,
            "tarjeta": self.card_id,
            "transaccion": self.transaction_id,
            "units": self.units
        }
        return c
