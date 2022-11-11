from peewee import *
from Models.Databases import maria


class Product(Model):
    name = CharField(50)
    description = CharField(255)
    price = DoubleField()

    class Meta:
        database = maria
        table_name = "products"

    def getinfo(self) -> dict:
        c: dict = {
            "id": self.id,
            "nombre": self.name,
            "descripcion": self.description,
            "precio": self.price
        }
        return c
