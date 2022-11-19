from peewee import *
from Models.Databases import maria
from Models.Transaction import Transaction
from Models.Product import Product


class Ticket(Model):
    transaction_id = ForeignKeyField(Transaction)
    product_id = ForeignKeyField(Product)
    subtotal = DoubleField()
    quantity = IntegerField()

    class Meta:
        database = maria
        table_name = "tickets"
        primary_key = False

    def getinfo(self) -> dict:
        c: dict = {
            "transaccion": self.transaction_id,
            "producto": self.product_id,
            "cantidad": self.quantity,
            "subtotal": self.subtotal
        }
        return c
