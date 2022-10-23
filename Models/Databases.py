from peewee import *

maria = MySQLDatabase(
    database="POS",
    user="root",
    password="mypass",
    host="127.0.0.1",
    port=3306
)


