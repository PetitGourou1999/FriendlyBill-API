def test_admin_redirect_to_login_when_not_authenticated(client):
    response = client.get('/admin/', follow_redirects=True)
    assert response.status_code == 200
    assert '/admin/login/' in response.request.base_url

def test_admin_login_not_authenticated(client):
    reponse = client.get('/admin/login/', follow_redirects=True)
    assert reponse.status_code == 200
    assert 'Submit' in reponse.text
    
def test_admin_authenticate_invalid_email_and_pwd(client):
    response = client.post('/admin/login/', data=dict(
        email='admin@admin.com',
        password='password'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert 'Invalid credentials' in response.text
    
def test_admin_authenticate_invalid_pwd(client, user_admin, user_admin_email):
    response = client.post('/admin/login/', data=dict(
        email=user_admin_email,
        password='password'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert 'Invalid credentials' in response.text

def test_admin_authenticate_not_admin(client, user_basic, user_basic_email, user_basic_password):
    response = client.post('/admin/login/', data=dict(
        email=user_basic_email,
        password=user_basic_password
    ), follow_redirects=True)
    assert response.status_code == 200
    assert 'Invalid credentials' in response.text
    
def test_admin_authenticate(client, user_admin, user_admin_email, user_admin_password):
    response = client.post('/admin/login/', data=dict(
        email=user_admin_email,
        password=user_admin_password
    ), follow_redirects=True)
    assert response.status_code == 200
    assert 'Welcome to the admin console !' in response.text
    
def test_admin_logout(client, user_admin, user_admin_email, user_admin_password):
    response = client.post('/admin/login/', data=dict(
        email=user_admin_email,
        password=user_admin_password
    ), follow_redirects=True)
    assert response.status_code == 200
    assert 'Welcome to the admin console !' in response.text
    
    response = client.get('/admin/logout/', follow_redirects=True)
    assert response.status_code == 200
    assert '/admin/login/' in response.request.base_url
