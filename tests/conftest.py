import pytest

from flask_jwt_extended import create_access_token

from app import app, db
from config import TestingConfig

from data.models import User, Bill, BillUser, BillItem, MODELS

@pytest.fixture
def application():
    app.config.from_object(TestingConfig())
    ctx = app.test_request_context()
    ctx.push()
    yield app
    ctx.pop()
    db.database.drop_tables(MODELS)
    db.database.create_tables(MODELS)    

@pytest.fixture()
def client(application):
    yield application.test_client()

@pytest.fixture()
def runner(application):
    yield application.test_cli_runner()
    
@pytest.fixture
def user_admin_email():
    return 'admin@admin.com'

@pytest.fixture
def user_admin_password():
    return 'SuperSecret'

@pytest.fixture
def bill_title():
    return 'DummyBill'

@pytest.fixture
def bill_item_title():
    return 'DummyItem'

@pytest.fixture
def bill_item_amount():
    return 30

@pytest.fixture
def user_admin(client, user_admin_email, user_admin_password):
    admin = User.get_by_email(user_admin_email)
    if admin is None:
        admin = User.create(firstname='John', surname='Doe', 
                           email=user_admin_email, 
                           password=user_admin_password, 
                           created_date='2023-01-01 00:00:00.000000', 
                           updated_date='2023-01-01 00:00:00.000000')
    yield admin

@pytest.fixture
def bill(client, bill_title):
    bill = Bill.get_by_title(bill_title)
    if not bill:
        bill = Bill.create(title=bill_title, 
                           created_date='2023-01-01 00:00:00.000000', 
                           updated_date='2023-01-01 00:00:00.000000')
    yield bill

@pytest.fixture
def bill_user(client, user_admin, bill):
    bill_user = BillUser.get_by_user_and_bill(user_admin, bill)
    if bill_user is None:
        bill_user = Bill.create(user=user_admin, bill=bill, is_owner=True,
                                created_date='2023-01-01 00:00:00.000000', 
                                updated_date='2023-01-01 00:00:00.000000')
    
    yield bill_user

@pytest.fixture
def bill_item(client, bill_user, bill_item_title, bill_item_amount):
    bill_item = BillItem.get_by_title(bill_item_title)
    if not bill_item:
        bill_item = BillItem.create(title=bill_item_title, amount=bill_item_amount,
                        bill_user=bill_user,
                        created_date='2023-01-01 00:00:00.000000', 
                        updated_date='2023-01-01 00:00:00.000000')
    yield bill_item

@pytest.fixture    
def user_admin_token_header(user_admin):
    access_token = create_access_token(identity=user_admin, expires_delta=False, fresh=True)
    return {'Authorization': 'Bearer {}'.format(access_token)}
