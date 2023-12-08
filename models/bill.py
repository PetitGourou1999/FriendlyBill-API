from peewee import *

class Bill(Model):
    id = AutoField()
    title = CharField()
    created_date = DateTimeField()
    updated_date = DateTimeField()