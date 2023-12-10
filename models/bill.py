import datetime

from peewee import *

class Bill(Model):
    id = AutoField()
    title = CharField()
    created_date = DateTimeField(default=datetime.datetime.now)
    updated_date = DateTimeField(default=datetime.datetime.now)