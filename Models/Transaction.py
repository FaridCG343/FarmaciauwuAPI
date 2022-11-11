from peewee import *
from Models.Databases import maria
from Models.Client import Client
from Models.Employee import Employee
from Models.Card import Card


class Transaction(Model):
    client_id = ForeignKeyField(Client)
    employee_id = ForeignKeyField(Employee)
    total = DoubleField()
    date = DateField()
    card_id = ForeignKeyField(Card)

    class Meta:
        database = maria
        table_name = "transactions"
