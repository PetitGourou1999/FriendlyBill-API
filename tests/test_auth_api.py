def test_register_no_body(client):
    response = client.post('/api/auth/register', json={})
    assert response.status_code == 422
    
def test_register_superadmin(client):
    response = client.post('/api/auth/register', json={
        'firstname': 'John',
        'surname': 'Doe',
        'email': 'john.doe@gmail.com',
        'password': 'SuperSecret',
        'is_superadmin': True
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Superadmins cannot be created this way'
    
def test_register(client):
    response = client.post('/api/auth/register', json={
        'firstname': 'John',
        'surname': 'Doe',
        'email': 'john.doe@gmail.com',
        'password': 'SuperSecret',
    })
    assert response.status_code == 201
    
def test_register_email_taken(client):
    body = {
        'firstname': 'John',
        'surname': 'Doe',
        'email': 'john.doe@gmail.com',
        'password': 'SuperSecret',
    }
    response = client.post('/api/auth/register', json=body)
    assert response.status_code == 201
    
    response = client.post('/api/auth/register', json=body)
    assert response.status_code == 400
    assert response.json['message'] == 'Email already taken'
    
def test_login_no_body(client):
    response = client.post('/api/auth/login', json={})
    assert response.status_code == 422
    
def test_login_invalid_credentials(client):
    response = client.post('/api/auth/login', json={
        'email': 'john.doe@gmail.com',
        'password': 'SuperSecret'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid email or password'
    
def test_login(client, user_admin, valid_user_admin_otp, user_admin_email, user_admin_password):
    response = client.post('/api/auth/login', json={
        'email': user_admin_email,
        'password': user_admin_password
    })
    assert response.status_code == 200
    assert response.json['token']
    
def test_delete_account_no_token(client):
    response = client.delete('/api/auth/account')
    assert response.status_code == 401
    
def test_delete_account(client, user_admin_token_header):
    response = client.delete('/api/auth/account', headers=user_admin_token_header)
    assert response.status_code == 204