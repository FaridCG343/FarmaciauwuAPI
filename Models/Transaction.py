from peewee import *
from Models.Databases import maria
from Models.Client import Client
from Models.Employee import Employee
from Models.Card import Card


class Transaction(Model):
    id_transaccion = IntegerField(primary_key=True)
    id_cliente = ForeignKeyField(Client, to_field="id_cliente")
    id_empleado = ForeignKeyField(Employee, to_field="id_empleado")
    total = DoubleField()
    fecha = DateField()
    id_tarjeta = ForeignKeyField(Card, to_field="id_tarjeta")

    class Meta:
        database = maria
        table_name = "transactions"
