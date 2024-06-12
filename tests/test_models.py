import datetime

from data.models import OTP

def test_flask_admin_user_properties(client, user_admin):
    assert user_admin.is_authenticated is True
    assert user_admin.is_active is True
    assert user_admin.is_anonymous is False
    
def test_user_str(client, user_admin):
    assert str(user_admin) == user_admin.email
    
def test_bill_str(client, bill):
    assert str(bill) == bill.title
    
def test_bill_user_str(client, bill_user_admin, user_admin_email, bill_title):
    assert str(bill_user_admin) == '{} : {}'.format(user_admin_email, bill_title)
    
def test_bill_item_str(client, bill_item):
    assert str(bill_item) == bill_item.title
    
def test_otp_blocked(client, user_admin):
    otp = OTP.create_or_update_otp(user_admin)
    otp.blocked_since = datetime.datetime.now()
    otp.save()
    assert otp.is_blocked is True

def test_otp_not_valid(client, user_admin):
    otp = OTP.create_or_update_otp(user_admin)
    otp.last_successful_attempt = (datetime.datetime.now() - datetime.timedelta(hours=144))
    otp.save()
    assert otp.is_still_valid is False

def test_otp_ok_attributes(client, user_admin, valid_user_admin_otp):
    assert valid_user_admin_otp.is_blocked is False
    assert valid_user_admin_otp.is_still_valid is True