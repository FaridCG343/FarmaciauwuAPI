from peewee import *
from Models.Databases import maria
from Models.Client import Client


class Card(Model):
    id_tarjeta = IntegerField(primary_key=True)
    id_cliente = ForeignKeyField(Client, to_field="id_cliente")
    fecha_registro = DateField()

    class Meta:
        database = maria
        table_name = "cards"

    def getinfo(self) -> dict:
        c: dict = {
            "id": self.id_tarjeta,
            "cliente": self.id_cliente,
            "fecha de registro": self.fecha_registro
        }
        return c
