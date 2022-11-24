from peewee import *
from Models.Databases import maria
from Models.Product import Product
from Models.Store import Store


class Stock(Model):
    product_id = ForeignKeyField(Product)
    store_id = ForeignKeyField(Store)
    available_products = IntegerField()

    class Meta:
        database = maria
        table_name = "stock"
        primary_key = False
