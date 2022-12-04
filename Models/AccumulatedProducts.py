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
        primary_key = CompositeKey('product_id', 'transaction_id')
        database = maria
        table_name = "accumulated_products"
