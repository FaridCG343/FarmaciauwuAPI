from peewee import *
from Models.Databases import maria


class Employee(Model):
    name = CharField(50)
    lastname = CharField(100)
    phoneNumber = CharField(15)

    class Meta:
        database = maria
        table_name = "employees"

    def getinfo(self) -> dict:
        c: dict = {
            "id": self.id,
            "nombre": self.name,
            "apellidos": self.lastname,
            "telefono": self.phoneNumber
        }
        return c

# generate_password_hash


class User(Model):
    employee_id = ForeignKeyField(Employee)
    password = CharField()
    is_admin = BooleanField()

    class Meta:
        database = maria
        table_name = "users"
        primary_key = False

    def getinfo(self) -> dict:
        c: dict = {
            "id": self.employee_id,
            "password": self.password,
            "is_admin": self.is_admin
        }

        return c
