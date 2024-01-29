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
        if query['password']:
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

 
class BillUser(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref='bills')
    bill = ForeignKeyField(Bill, backref='users')
    is_owner = BooleanField(default=False)

    @classmethod
    def get_by_user(self, user):
        query = self.select().join(User).where(User.id == user.id).execute()
        return list(query)
        
    @classmethod
    def get_by_user_and_bill(self, user, bill):
        return self.get_or_none(BillUser.user == user, BillUser.bill == bill)
    
    def __str__(self) -> str:
        return '{} : {}'.format(self.user.email, self.bill.title)


class BillItem(BaseModel):
    id = AutoField()
    title = CharField()
    bill_user = ForeignKeyField(BillUser, backref='items')
    
    @classmethod
    def get_by_user(self, user):
        query = self.select().join(BillUser).join(User).where(User.id == user.id).execute()
        return list(query)
    
    def __str__(self) -> str:
        return self.title
    

def register_database(db):
    db.database.bind([User, Bill, BillUser, BillItem])