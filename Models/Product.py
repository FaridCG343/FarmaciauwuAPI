from peewee import *
from Models.Databases import maria


class Product(Model):
    name = CharField(50)
    description = CharField(255)
    price = DoubleField()
    status = CharField(100)

    class Meta:
        database = maria
        table_name = "products"
