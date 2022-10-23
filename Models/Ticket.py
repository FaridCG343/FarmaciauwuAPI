from peewee import *
from Models.Databases import maria
from Models.Transaction import Transaction
from Models.Product import Product


class Ticket(Model):
    id_transaccion = ForeignKeyField(Transaction, to_field="id_transaccion")
    id_producto = ForeignKeyField(Product, to_field="id_producto")
    subtotal = DoubleField()
    cantidad = IntegerField()

    class Meta:
        database = maria
        table_name = "clients"
        primary_key = False

    def getinfo(self) -> dict:
        c: dict = {
            "transaccion": self.id_transaccion,
            "producto": self.id_producto,
            "cantidad": self.cantidad,
            "subtotal": self.subtotal
        }
        return c
