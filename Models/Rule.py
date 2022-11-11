from peewee import *
from Models.Databases import maria
from Models.Product import Product


class Rule(Model):
    product_id = ForeignKeyField(Product)
    description = CharField()
    active = BooleanField()
    type = CharField(50)
    purchaseX = IntegerField()
    giftY = IntegerField()
    discount = IntegerField()

    class Meta:
        database = maria
        table_name = "rules"

    def getinfo(self) -> dict:
        c: dict = {
            "id": self.id,
            "producto": self.product_id,
            "descripcion": self.description,
            "activo": self.active,
            "tipo": self.type,
            "compra": self.purchaseX,
            "gana": self.giftY,
            "descuento": self.discount
        }
        return c
