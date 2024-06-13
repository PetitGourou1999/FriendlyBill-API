import datetime
import pytest

from flask_jwt_extended import create_access_token

from app import app, db
from config import TestingConfig

from data.models import User, OTP, Bill, BillUser, BillItem, MODELS

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
    return 'admin@gmail.com'

@pytest.fixture
def user_admin_password():
    return 'SuperSecret'

@pytest.fixture
def user_basic_email():
    return 'user@gmail.com'

@pytest.fixture
def user_basic_password():
    return 'SuperSecret'

@pytest.fixture
def other_user_basic_email():
    return 'other.user@gmail.com'

@pytest.fixture
def other_user_basic_password():
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
                           is_superadmin=True,
                           created_date='2023-01-01 00:00:00.000000', 
                           updated_date='2023-01-01 00:00:00.000000')
    yield admin

@pytest.fixture
def user_basic(client, user_basic_email, user_basic_password):
    user = User.get_by_email(user_basic_email)
    if user is None:
        user = User.create(firstname='John', surname='Doe', 
                           email=user_basic_email, 
                           password=user_basic_password, 
                           created_date='2023-01-01 00:00:00.000000', 
                           updated_date='2023-01-01 00:00:00.000000')
    yield user

@pytest.fixture
def other_user_basic(client, other_user_basic_email, other_user_basic_password):
    user = User.get_by_email(other_user_basic_email)
    if user is None:
        user = User.create(firstname='John', surname='Doe', 
                           email=other_user_basic_email, 
                           password=other_user_basic_password, 
                           created_date='2023-01-01 00:00:00.000000', 
                           updated_date='2023-01-01 00:00:00.000000')
    yield user

@pytest.fixture
def valid_user_admin_otp(client, user_admin):
    otp = OTP.create_or_update_otp(user=user_admin)
    otp.last_successful_attempt = datetime.datetime.now()
    otp.save()
    yield otp

@pytest.fixture
def three_attempts_user_admin_otp(client, user_admin):
    otp = OTP.create_or_update_otp(user=user_admin)
    otp.num_attempts = 3
    otp.save()
    yield otp

@pytest.fixture
def blocked_user_admin_otp(client, user_admin):
    otp = OTP.create_or_update_otp(user=user_admin)
    otp.num_attempts = 4
    otp.blocked_since = datetime.datetime.now()
    otp.save()
    yield otp

@pytest.fixture
def invalid_user_admin_otp(client, user_admin):
    otp = OTP.create_or_update_otp(user=user_admin)
    otp.last_successful_attempt = datetime.datetime.now() - datetime.timedelta(hours=144)
    otp.save()
    yield otp

@pytest.fixture
def bill(client, bill_title):
    bill = Bill.get_by_title(bill_title)
    if not bill:
        bill = Bill.create(title=bill_title, 
                           created_date='2023-01-01 00:00:00.000000', 
                           updated_date='2023-01-01 00:00:00.000000')
    yield bill

@pytest.fixture
def bill_user_admin(client, user_admin, bill):
    bill_user = BillUser.get_by_user_and_bill(user_admin, bill)
    if bill_user is None:
        bill_user = BillUser.create(user=user_admin, bill=bill, is_owner=True,
                                created_date='2023-01-01 00:00:00.000000', 
                                updated_date='2023-01-01 00:00:00.000000')
    
    yield bill_user

@pytest.fixture
def bill_user_basic(client, user_basic, bill):
    bill_user = BillUser.get_by_user_and_bill(user_basic, bill)
    if bill_user is None:
        bill_user = BillUser.create(user=user_basic, bill=bill, is_owner=False,
                                created_date='2023-01-01 00:00:00.000000', 
                                updated_date='2023-01-01 00:00:00.000000')
    
    yield bill_user

@pytest.fixture
def bill_item(client, bill_user_admin, bill_item_title, bill_item_amount):
    bill_item = BillItem.get_by_title(bill_item_title)
    if not bill_item:
        bill_item = BillItem.create(title=bill_item_title, amount=bill_item_amount,
                        bill_user=bill_user_admin,
                        created_date='2023-01-01 00:00:00.000000', 
                        updated_date='2023-01-01 00:00:00.000000')
    yield bill_item

@pytest.fixture
def all_data(client, user_admin, valid_user_admin_otp, user_basic, other_user_basic, bill, bill_user_admin, bill_user_basic, bill_item):
    pass
    
@pytest.fixture    
def user_admin_token_header(user_admin):
    access_token = create_access_token(identity=user_admin, expires_delta=False, fresh=True)
    return {'Authorization': 'Bearer {}'.format(access_token)}

@pytest.fixture    
def user_basic_token_header(user_basic):
    access_token = create_access_token(identity=user_basic, expires_delta=False, fresh=True)
    return {'Authorization': 'Bearer {}'.format(access_token)}

@pytest.fixture    
def other_user_basic_token_header(other_user_basic):
    access_token = create_access_token(identity=other_user_basic, expires_delta=False, fresh=True)
    return {'Authorization': 'Bearer {}'.format(access_token)}