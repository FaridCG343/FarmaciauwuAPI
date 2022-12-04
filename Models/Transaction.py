from peewee import *
from Models.Databases import maria
from Models.Employee import Employee
from Models.Card import Card


class Transaction(Model):
    employee_id = ForeignKeyField(Employee)
    total = DoubleField()
    date = DateField()
    card_id = ForeignKeyField(Card)
    status = CharField(50)

    class Meta:
        database = maria
        table_name = "transactions"
