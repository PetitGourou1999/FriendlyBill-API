from data.models import Bill, BillUser, BillItem

def test_get_bills_no_token(client):
    response = client.get('/api/bills')
    assert response.status_code == 401

def test_get_bills_no_bills(client, user_admin, user_admin_token_header):
    response = client.get('/api/bills', headers=user_admin_token_header)
    assert response.status_code == 400
    assert response.json['message'] == 'Not found'

def test_get_bills(client, all_data, user_admin_token_header, bill_title):
    response = client.get('/api/bills', headers=user_admin_token_header)
    assert response.status_code == 200
    assert bill_title in response.text

def test_create_bill_no_token(client):
    response = client.post('/api/bills', json={})
    assert response.status_code == 401
    
def test_create_bill_no_body(client, user_admin, user_admin_token_header):
    response = client.post('/api/bills', headers=user_admin_token_header, json={})
    assert response.status_code == 422
    
def test_create_bill(client, user_admin, user_admin_token_header):
    response = client.post('/api/bills', headers=user_admin_token_header, json={
        'title': 'Dummy'
    })
    assert response.status_code == 201
    
    created_bill = Bill.get_by_title('Dummy')
    assert created_bill
    created_bill_user = BillUser.get_by_user_and_bill(user_admin, created_bill[0])
    assert created_bill_user
    assert created_bill_user.is_owner is True

def test_delete_bill_no_id(client, user_admin, user_admin_token_header):
    response = client.delete('/api/bills', headers=user_admin_token_header)
    assert response.status_code == 400

def test_delete_bill_no_token(client):
    response = client.delete('/api/bills?id=1')
    assert response.status_code == 401

def test_delete_bill_not_found(client, user_admin, user_admin_token_header):
    response = client.delete('/api/bills?id=1', headers=user_admin_token_header)
    assert response.status_code == 400
    assert response.json['message'] == 'Not found'
    
def test_delete_bill_not_owner(client, all_data, user_basic_token_header):
    response = client.delete('/api/bills?id=1', headers=user_basic_token_header)
    assert response.status_code == 400
    assert response.json['message'] == 'You are not the owner of this bill'

def test_delete_bill(client, all_data, user_admin_token_header):
    response = client.delete('/api/bills?id=1', headers=user_admin_token_header)
    assert response.status_code == 204

def test_invite_user_no_token(client):
    response = client.post('/api/bills/users', json={})
    assert response.status_code == 401
    
def test_invite_user_no_body(client, user_admin, user_admin_token_header):
    response = client.post('/api/bills/users', headers=user_admin_token_header, json={})
    assert response.status_code == 422
    
def test_invite_user_user_does_not_exist(client, all_data, user_admin_token_header):
    response = client.post('/api/bills/users', headers=user_admin_token_header, json={
        'user_email': 'nobody@gmail.com',
        'bill_id': '1'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'User does not exist'

def test_invite_user_bill_does_not_exist(client, all_data, user_basic_email, user_admin_token_header):
    response = client.post('/api/bills/users', headers=user_admin_token_header, json={
        'user_email': user_basic_email,
        'bill_id': '2'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Bill does not exist'

def test_invite_user_not_owner(client, all_data, user_basic_email, user_basic_token_header):
    response = client.post('/api/bills/users', headers=user_basic_token_header, json={
        'user_email': user_basic_email,
        'bill_id': '1'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'You are not the owner of this bill'

def test_invite_user_already_invited(client, all_data, user_basic_email, user_admin_token_header):
    response = client.post('/api/bills/users', headers=user_admin_token_header, json={
        'user_email': user_basic_email,
        'bill_id': '1'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'User has already been invited'
    
def test_invite_user(client, all_data, other_user_basic, bill, other_user_basic_email, user_admin_token_header):
    response = client.post('/api/bills/users', headers=user_admin_token_header, json={
        'user_email': other_user_basic_email,
        'bill_id': '1'
    })
    assert response.status_code == 201
    
    bill_user = BillUser.get_by_user_and_bill(other_user_basic, bill)
    assert bill_user
    assert bill_user.is_owner is False
    
def test_delete_bill_user_no_token(client):
    response = client.delete('/api/bills/users?id=1')
    assert response.status_code == 401
    
def test_delete_bill_user_no_id(client, user_admin, user_admin_token_header):
    response = client.delete('/api/bills/users', headers=user_admin_token_header)
    assert response.status_code == 400
    
def test_delete_bill_user_not_found(client, all_data, user_admin_token_header):
    response = client.delete('/api/bills/users?id=99', headers=user_admin_token_header)
    assert response.status_code == 400
    assert response.json['message'] == 'Not found'

def test_delete_bill_user_not_owner(client, all_data, user_basic_token_header):
    response = client.delete('/api/bills/users?id=1', headers=user_basic_token_header)
    assert response.status_code == 400
    assert response.json['message'] == 'You are not the owner of this bill'

def test_delete_bill_user(client, all_data, user_admin_token_header):
    response = client.delete('/api/bills/users?id=2', headers=user_admin_token_header)
    assert response.status_code == 204

def test_get_bill_items_no_token(client):
    response = client.get('/api/bills/items')
    assert response.status_code == 401

def test_get_bill_items_not_found(client, all_data, user_basic_token_header):
    response = client.get('/api/bills/items', headers=user_basic_token_header)
    assert response.status_code == 400
    assert response.json['message'] == 'Not found'

def test_get_bill_items(client, all_data, bill_item_title, user_admin_token_header):
    response = client.get('/api/bills/items', headers=user_admin_token_header)
    assert response.status_code == 200
    assert bill_item_title in response.text
    
def test_create_bill_item_no_token(client):
    response = client.post('/api/bills/items', json={})
    assert response.status_code == 401

def test_create_bill_item_no_body(client, user_admin, user_admin_token_header):
    response = client.post('/api/bills/items', headers=user_admin_token_header, json={})
    assert response.status_code == 422
    
def test_create_bill_item_bill_does_not_exist(client, all_data, user_admin_token_header):
    response = client.post('/api/bills/items', headers=user_admin_token_header, json={
        'title': 'Dummy',
        'amount': '20',
        'bill_id': '99'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Bill does not exist'

def test_create_bill_item_not_invited(client, all_data, other_user_basic_token_header):
    response = client.post('/api/bills/items', headers=other_user_basic_token_header, json={
        'title': 'Dummy',
        'amount': '20',
        'bill_id': '1'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'You cannot add items to this bill'

def test_create_bill_item(client, all_data, user_basic_token_header):
    response = client.post('/api/bills/items', headers=user_basic_token_header, json={
        'title': 'DummyTitle',
        'amount': '20',
        'bill_id': '1'
    })
    assert response.status_code == 201
    
    bill_item = BillItem.get_by_title('DummyTitle')
    assert bill_item

def test_delete_bill_item_no_token(client):
    response = client.delete('/api/bills/items?id=1')
    assert response.status_code == 401
    
def test_delete_bill_item_no_id(client, user_admin, user_admin_token_header):
    response = client.delete('/api/bills/items', headers=user_admin_token_header)
    assert response.status_code == 400
    
def test_delete_bill_item_not_found(client, all_data, user_admin_token_header):
    response = client.delete('/api/bills/items?id=99', headers=user_admin_token_header)
    assert response.status_code == 400
    assert response.json['message'] == 'Not found'
    
def test_delete_bill_item(client, all_data, user_admin_token_header):
    response = client.delete('/api/bills/items?id=1', headers=user_admin_token_header)
    assert response.status_code == 204
