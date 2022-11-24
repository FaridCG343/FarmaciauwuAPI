from peewee import *
from Models.Databases import maria


class Client(Model):
    name = CharField(50)
    lastname = CharField(100)
    phoneNumber = CharField(15)
    email = CharField(255)
    address = CharField(255)

    class Meta:
        database = maria
        table_name = "clients"
