from peewee import *
from Models.Databases import maria
from Models.Client import Client


class Card(Model):
    client_id = ForeignKeyField(Client)
    register_date = DateField()

    class Meta:
        database = maria
        table_name = "cards"
