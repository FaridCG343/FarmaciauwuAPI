from peewee import *
from Models.Databases import maria


class Store(Model):
    name = CharField(50)
    address = CharField(200)
    active = BooleanField()

    class Meta:
        database = maria
        table_name = "stores"

    def todict(self):
        return {
            "name": self.name,
            "address": self.address,
            "active": self.active
        }
