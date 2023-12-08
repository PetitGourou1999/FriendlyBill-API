from peewee import *
from models.user import User
from models.bill import Bill

class BillItem(Model):
    id = AutoField()
    title = CharField()
    created_date = DateTimeField()
    updated_date = DateTimeField()
    user = ForeignKeyField(User, backref='items')
    bill = ForeignKeyField(Bill, backref='items')