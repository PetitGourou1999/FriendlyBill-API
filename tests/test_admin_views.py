def login(api_client, admin_email, admin_password):
    response = api_client.post('/admin/login/', data=dict(
        email=admin_email,
        password=admin_password
    ), follow_redirects=True)
    
def test_users_view(client, user_admin, user_admin_email, user_admin_password):
    login(client, user_admin_email, user_admin_password)
    response = client.get('/admin/user/', follow_redirects=True)
    assert response.status_code == 200

def test_otps_view(client, user_admin, user_admin_email, user_admin_password):
    login(client, user_admin_email, user_admin_password)
    response = client.get('/admin/otp/', follow_redirects=True)
    assert response.status_code == 200

def test_bills_view(client, user_admin, user_admin_email, user_admin_password):
    login(client, user_admin_email, user_admin_password)
    response = client.get('/admin/bill/', follow_redirects=True)
    assert response.status_code == 200

def test_billusers_view(client, user_admin, user_admin_email, user_admin_password):
    login(client, user_admin_email, user_admin_password)
    response = client.get('/admin/billuser/', follow_redirects=True)
    assert response.status_code == 200

def test_billitems_view(client, user_admin, user_admin_email, user_admin_password):
    login(client, user_admin_email, user_admin_password)
    response = client.get('/admin/billitem/', follow_redirects=True)
    assert response.status_code == 200
