from models.user import User
from models.bill import Bill
from models.bill_item import BillItem

def _insert_user():
    return User.create(firstname='John', surname='Doe', email='john.doe@gmail.com', created_date='2023-01-01 00:00:00.000000', updated_date='2023-01-01 00:00:00.000000')

def _insert_bill():
    return Bill.create(title='Dummy', created_date='2023-01-01 00:00:00.000000', updated_date='2023-01-01 00:00:00.000000')

def _insert_bill_item(user, bill):
    if(isinstance(user, User) & isinstance(bill, Bill)):
        return BillItem.create(title='Dummy', created_date='2023-01-01 00:00:00.000000', updated_date='2023-01-01 00:00:00.000000', user=user, bill=bill)

def insert_data():
    user = _insert_user()
    bill = _insert_bill()
    _insert_bill_item(user, bill)