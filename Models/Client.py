from peewee import *
from Models.Databases import maria


class Client(Model):
    id_cliente = IntegerField(primary_key=True)
    nombre = CharField(50)
    apellidos = CharField(100)
    telefono = CharField(15)
    correo = CharField(255)
    direccion = CharField(255)

    class Meta:
        database = maria
        table_name = "clients"

    def getinfo(self) -> dict:
        c: dict = {
            "id": self.id_cliente,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "telefono": self.telefono,
            "correo": self.correo,
            "direccion": self.direccion
        }
        return c
