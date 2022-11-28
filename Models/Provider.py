from peewee import *
from Models.Databases import maria


class Provider(Model):
    name = CharField()
    phone_number = CharField()
    email = CharField()

    class Meta:
        database = maria
        table_name = "providers"
