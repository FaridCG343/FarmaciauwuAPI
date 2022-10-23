from peewee import *
from Models.Databases import maria
from Models.Product import Product


class Rule(Model):
    id_regla = IntegerField(primary_key=True)
    id_producto = ForeignKeyField(Product)
    descripcion = CharField()
    activo = BooleanField()
    tipo = CharField(50)
    compraX = IntegerField()
    regaloY = IntegerField()
    descuento = IntegerField()

    class Meta:
        database = maria
        table_name = "rules"

    def getinfo(self) -> dict:
        c: dict = {
            "id": self.id_producto,
            "producto": self.id_producto,
            "descripcion": self.descripcion,
            "activo": self.activo,
            "tipo": self.tipo,
            "compra": self.compraX,
            "gana": self.regaloY,
            "descuento": self.descuento
        }
        return c
