from peewee import *
from Models.Databases import maria
from Models.Product import Product
from Models.Card import Card
from Models.Transaction import Transaction


class AccumulatedProducts(Model):
    id_producto = ForeignKeyField(Product, to_field="id_producto")
    id_tarjeta = ForeignKeyField(Card, to_field="id_tarjeta")
    id_transaccion = ForeignKeyField(Transaction, to_field="id_transaccion")
    units = IntegerField()

    class Meta:
        database = maria
        table_name = "accumulated_products"

    def getinfo(self) -> dict:
        c: dict = {
            "producto": self.id_producto,
            "tarjeta": self.id_tarjeta,
            "transaccion": self.id_transaccion,
            "units": self.units
        }
        return c
