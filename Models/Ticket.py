from peewee import *
from Models.Databases import maria
from Models.Transaction import Transaction
from Models.Product import Product
from Models.Store import Store


class Ticket(Model):
    transaction_id = ForeignKeyField(Transaction)
    product_id = ForeignKeyField(Product)
    subtotal = DoubleField()
    units = IntegerField()
    store_id = ForeignKeyField(Store)

    class Meta:
        database = maria
        table_name = "tickets"
        primary_key = False
