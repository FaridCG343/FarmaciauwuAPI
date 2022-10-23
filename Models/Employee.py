from peewee import *
from Models.Databases import maria


class Employee(Model):
    id_empleado = IntegerField(primary_key=True)
    nombre = CharField(50)
    apellidos = CharField(100)
    telefono = CharField(15)

    class Meta:
        database = maria
        table_name = "employees"

    def getinfo(self) -> dict:
        c: dict = {
            "id": self.id_empleado,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "telefono": self.telefono
        }
        return c
