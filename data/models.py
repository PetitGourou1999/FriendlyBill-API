import bcrypt
import datetime

from peewee import *

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
        return self.get(User.email == email)
    
    @classmethod
    def encrypt_password(password):
        hashed_password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
        return hashed_password.decode()

    @classmethod
    def login(self, email, decrypted_password):
        user = self.get_by_email(email)
        if not user or not (bcrypt.hashpw(bytes(decrypted_password, 'utf-8'), bytes(user.password, 'utf-8')) == bytes(user.password, 'utf-8')):
            return
        return user


class Bill(BaseModel):
    id = AutoField()
    title = CharField()
    

class BillItem(BaseModel):
    id = AutoField()
    title = CharField()
    user = ForeignKeyField(User, backref='items')
    bill = ForeignKeyField(Bill, backref='items')