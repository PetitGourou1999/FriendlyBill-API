import datetime

from peewee import *

from custom_exceptions import UserBlockedException
from shortcuts import encrypt_password, generate_otp

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
    def get_superadmins(self):
        query = self.select().where(User.is_superadmin == True).execute()
        return list(query)
    
    @classmethod
    def create(cls, **query):
        if query['password']:
            query['password'] = encrypt_password(query['password'])
        return super().create(**query)
    
    def __str__(self) -> str:
        return self.email

    def __unicode__(self):
        return self.email


class OTP(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref='otp', on_delete='CASCADE', unique=True)
    otp = IntegerField(null=True)
    num_attempts = IntegerField(default=0)
    last_successful_attempt = DateTimeField(null=True)
    blocked_since = DateTimeField(null=True)
    
    @classmethod
    def get_by_user(self, user):
        return self.get_or_none(OTP.user == user)
    
    @classmethod
    def create_or_update_otp(self, user):
        otp = self.get_by_user(user)
        if not otp:
            otp = OTP(user=user, otp=generate_otp(), num_attempts=1)
            otp.save()
            return otp
        
        if otp.is_blocked:
            raise UserBlockedException()
        else:
            otp.blocked_since = None
        
        otp.otp = generate_otp()
        otp.num_attempts = otp.num_attempts + 1
        otp.save()
        return otp
    
    @property
    def is_blocked(self):
        blocked_since = self.blocked_since
        if blocked_since:
            if type(blocked_since) is str:
                blocked_since = datetime.datetime.fromisoformat(blocked_since)
            if (blocked_since + datetime.timedelta(hours=1)) > datetime.datetime.now():
                return True
        return False

    @property
    def is_still_valid(self):
        user_last_successful_attempt = self.last_successful_attempt
        if type(user_last_successful_attempt) is str:
            user_last_successful_attempt = datetime.datetime.fromisoformat(user_last_successful_attempt)
        if (user_last_successful_attempt + datetime.timedelta(hours=72)) < datetime.datetime.now():
            return False
        return True

        
    def __str__(self) -> str:
        return '{} - {}'.format(self.user.email, self.otp)

    
class Bill(BaseModel):
    id = AutoField()
    title = CharField()

    @classmethod
    def get_by_title(self, title):
        query = self.select().where(Bill.title == title).execute()
        return list(query)
    
    def __str__(self) -> str:
        return self.title

 
class BillUser(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref='bills', on_delete='CASCADE')
    bill = ForeignKeyField(Bill, backref='users', on_delete='CASCADE')
    is_owner = BooleanField(default=False)

    @classmethod
    def get_by_user(self, user):
        query = self.select().join(User).where(User.id == user.id).execute()
        return list(query)
        
    @classmethod
    def get_by_user_and_bill(self, user, bill):
        return self.get_or_none(BillUser.user == user, BillUser.bill == bill)
    
    class Meta:
        indexes = (
            (('user', 'bill'), True),
        )
    
    def __str__(self) -> str:
        return '{} : {}'.format(self.user.email, self.bill.title)


class BillItem(BaseModel):
    id = AutoField()
    title = CharField()
    amount = DoubleField()
    bill_user = ForeignKeyField(BillUser, backref='items', on_delete='CASCADE')
    
    @classmethod
    def get_by_user(self, user):
        query = self.select().join(BillUser).join(User).where(User.id == user.id).execute()
        return list(query)
    
    @classmethod
    def get_by_title(self, title):
        query = self.select().where(BillItem.title == title).execute()
        return list(query)
    
    def __str__(self) -> str:
        return self.title
    

MODELS = [User, OTP, Bill, BillUser, BillItem]

def register_database(db):
    db.database.bind(MODELS)