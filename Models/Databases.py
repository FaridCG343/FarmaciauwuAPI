from peewee import MySQLDatabase
from os import getenv
from dotenv import load_dotenv

load_dotenv()

database = getenv("DATABASE")
user = getenv("USER_DB")
password = getenv("PASSWORD")
host = getenv("HOST")
port = getenv("PORT")

maria = MySQLDatabase(
    database=database,
    user=user,
    password=password,
    host=host,
    port=int(port)
)


