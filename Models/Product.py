from peewee import *
from Models.Databases import maria


class Product(Model):
    id_producto = IntegerField(primary_key=True)
    nombre = CharField(50)
    descripcion = CharField(255)
    precio = DoubleField()

    class Meta:
        database = maria
        table_name = "products"

    def getinfo(self) -> dict:
        c: dict = {
            "id": self.id_producto,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio
        }
        return c
