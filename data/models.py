import datetime

from peewee import *

from shortcuts import encrypt_password

class BaseModel(Model):
    created_date = DateTimeField(default=datetime.datetime.now)
    updated_date = DateTimeField(default=datetime.datetime.now)


class User(BaseModel):
    id = AutoField()
    firstname = CharField()
    surname = CharField()
    email = CharField(unique=True)
    password = CharField()

    @classmethod
    def get_by_email(self, email):
        return self.get_or_none(User.email == email)
    
    @classmethod
    def create(cls, **query):
        if query['password'] is not None:
            query['password'] = encrypt_password(query['password'])
        return super().create(**query)    


class Bill(BaseModel):
    id = AutoField()
    title = CharField()
    

class BillItem(BaseModel):
    id = AutoField()
    title = CharField()
    user = ForeignKeyField(User, backref='items')
    bill = ForeignKeyField(Bill, backref='items')