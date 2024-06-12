from data.models import User, Bill

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