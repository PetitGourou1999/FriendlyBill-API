from peewee import *

class User(Model):
    id = AutoField()
    firstname = CharField()
    surname = CharField()
    email = CharField()
    created_date = DateTimeField()
    updated_date = DateTimeField()