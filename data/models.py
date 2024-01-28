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
    is_superadmin = BooleanField(default=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @classmethod
    def get_by_email(self, email):
        return self.get_or_none(User.email == email)
    
    @classmethod
    def create(cls, **query):
        if query['password'] is not None:
            query['password'] = encrypt_password(query['password'])
        return super().create(**query)
    
    def __str__(self) -> str:
        return self.email

    def __unicode__(self):
        return self.email


class Bill(BaseModel):
    id = AutoField()
    title = CharField()

    def __str__(self) -> str:
        return self.title
    

class BillItem(BaseModel):
    id = AutoField()
    title = CharField()
    user = ForeignKeyField(User, backref='items')
    bill = ForeignKeyField(Bill, backref='items')

    def __str__(self) -> str:
        return self.title