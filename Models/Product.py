from peewee import *
from Models.Databases import maria


class Product(Model):
    name = CharField(50)
    description = CharField(255)
    price = DoubleField()

    class Meta:
        database = maria
        table_name = "products"

    def todict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price
        }
