from peewee import *
from Models.Databases import maria
from Models.Store import Store
from Models.Product import Product
from Models.Provider import Provider


class StockLogs(Model):
    provider_id = ForeignKeyField(Provider)
    product_id = ForeignKeyField(Product)
    store_id = ForeignKeyField(Store)
    quantity = IntegerField()
    date = DateField()

    class Meta:
        database = maria
        table_name = "stock_logs"
        primary_key = False
