from peewee import *
from Models.Databases import maria
from Models.Store import Store


class Employee(Model):
    name = CharField(50)
    lastname = CharField(100)
    phoneNumber = CharField(15)

    class Meta:
        database = maria
        table_name = "employees"

# generate_password_hash


class User(Model):
    employee_id = ForeignKeyField(Employee)
    password = CharField()
    position = CharField()
    store_id = ForeignKeyField(Store)
    userName = CharField(100, unique=True)

    class Meta:
        database = maria
        table_name = "users"
        primary_key = False
