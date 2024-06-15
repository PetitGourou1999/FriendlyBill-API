from data.models import User, OTP
from shortcuts import check_password

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
    assert User.get_by_email('john.doe@gmail.com') is None
    
def test_register(client):
    response = client.post('/api/auth/register', json={
        'firstname': 'John',
        'surname': 'Doe',
        'email': 'john.doe@gmail.com',
        'password': 'SuperSecret',
    })
    assert response.status_code == 201
    assert User.get_by_email('john.doe@gmail.com') is not None
    
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
    
def test_login_user_blocked(client, user_admin, blocked_user_admin_otp, user_admin_email, user_admin_password):
    response = client.post('/api/auth/login', json={
        'email': user_admin_email,
        'password': user_admin_password
    })
    assert response.status_code == 500
    assert response.json['message'] == 'User is blocked'

def test_login_need_to_revalidate_otp(client, user_admin, invalid_user_admin_otp, user_admin_email, user_admin_password):
    response = client.post('/api/auth/login', json={
        'email': user_admin_email,
        'password': user_admin_password
    })
    assert response.status_code == 500
    assert response.json['message'] == 'Need to revalidate OTP'

def test_login(client, user_admin, valid_user_admin_otp, user_admin_email, user_admin_password):
    response = client.post('/api/auth/login', json={
        'email': user_admin_email,
        'password': user_admin_password
    })
    assert response.status_code == 200
    assert response.json['token']
    
def test_send_otp_no_body(client):
    response = client.post('/api/auth/otp/send', json={})
    assert response.status_code == 422
    
def test_send_otp_invalid_credentials(client):
    response = client.post('/api/auth/otp/send', json={
        'email': 'john.doe@gmail.com',
        'password': 'SuperSecret'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid email or password'

def test_send_otp_user_already_blocked(client, user_admin, user_admin_email, user_admin_password, blocked_user_admin_otp):
    response = client.post('/api/auth/otp/send', json={
        'email': user_admin_email,
        'password': user_admin_password
    })
    assert response.status_code == 500
    assert response.json['message'] == 'User is blocked'

def test_send_otp_user_now_blocked(client, user_admin, user_admin_email, user_admin_password, three_attempts_user_admin_otp):
    response = client.post('/api/auth/otp/send', json={
        'email': user_admin_email,
        'password': user_admin_password
    })
    assert response.status_code == 500
    assert response.json['message'] == 'User is blocked'
    
    otp = OTP.get_by_user(user_admin)
    assert otp.blocked_since is not None
    assert otp.is_blocked is True
    
def test_send_otp_never_asked(client, user_admin, user_admin_email, user_admin_password):
    response = client.post('/api/auth/otp/send', json={
        'email': user_admin_email,
        'password': user_admin_password
    })
    assert response.status_code == 201
    assert response.json['email'] == user_admin_email
    
    assert OTP.get_by_user(user_admin) is not None

def test_send_otp_with_invalid_password(client, user_admin, user_admin_email, valid_user_admin_otp):
    response = client.post('/api/auth/otp/send', json={
        'email': user_admin_email,
        'password': 'NotAPassword'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid email or password'

def test_send_otp_with_password(client, user_admin, user_admin_email, user_admin_password, valid_user_admin_otp):
    response = client.post('/api/auth/otp/send', json={
        'email': user_admin_email,
        'password': user_admin_password
    })
    assert response.status_code == 201
    assert response.json['email'] == user_admin_email
    
    assert OTP.get_by_user(user_admin) is not None

def test_send_otp_without_password(client, user_admin, user_admin_email, user_admin_password, valid_user_admin_otp):
    response = client.post('/api/auth/otp/send', json={
        'email': user_admin_email,
    })
    assert response.status_code == 201
    assert response.json['email'] == user_admin_email
    
    assert OTP.get_by_user(user_admin) is not None

def test_validate_otp_no_body(client):
    response = client.post('/api/auth/otp/validate', json={})
    assert response.status_code == 422
    
def test_validate_otp_invalid_credentials(client):
    response = client.post('/api/auth/otp/validate', json={
        'email': 'john.doe@gmail.com',
        'password': 'SuperSecret',
        'otp': '123456'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid email or password'

def test_validate_otp_not_found(client, user_admin, user_admin_email, user_admin_password):
    response = client.post('/api/auth/otp/validate', json={
        'email': user_admin_email,
        'password': user_admin_password,
        'otp': '123456'
    })
    assert response.status_code == 500
    assert response.json['message'] == 'OTP not found'

def test_validate_otp_user_already_blocked(client, user_admin, user_admin_email, user_admin_password, blocked_user_admin_otp):
    response = client.post('/api/auth/otp/validate', json={
        'email': user_admin_email,
        'password': user_admin_password,
        'otp': '123456'
    })
    assert response.status_code == 500
    assert response.json['message'] == 'User is blocked'

def test_validate_otp_failed(client, user_admin, user_admin_email, user_admin_password):
    response = client.post('/api/auth/otp/send', json={
        'email': user_admin_email,
        'password': user_admin_password
    })
    assert response.status_code == 201
    
    response = client.post('/api/auth/otp/validate', json={
        'email': user_admin_email,
        'password': user_admin_password,
        'otp': 'WILLFAIL'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'OTP challenge failed'
    
    otp = OTP.get_by_user(user_admin)
    assert otp.last_successful_attempt is None

def test_validate_otp_with_invalid_password(client, user_admin, user_admin_email):
    response = client.post('/api/auth/otp/validate', json={
        'email': user_admin_email,
        'password': 'NotAPassword',
        'otp': '123456'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid email or password'
    
def test_validate_otp_with_password(client, user_admin, user_admin_email, user_admin_password):
    response = client.post('/api/auth/otp/send', json={
        'email': user_admin_email,
        'password': user_admin_password
    })
    assert response.status_code == 201
    
    otp = OTP.get_by_user(user_admin)
    response = client.post('/api/auth/otp/validate', json={
        'email': user_admin_email,
        'password': user_admin_password,
        'otp': otp.otp
    })
    assert response.status_code == 200
    assert response.json['token']
    
    otp = OTP.get_by_user(user_admin)
    assert otp.last_successful_attempt is not None
    assert otp.num_attempts == 0

def test_validate_otp_without_password(client, user_admin, user_admin_email, user_admin_password):
    response = client.post('/api/auth/otp/send', json={
        'email': user_admin_email,
        'password': user_admin_password
    })
    assert response.status_code == 201
    
    otp = OTP.get_by_user(user_admin)
    response = client.post('/api/auth/otp/validate', json={
        'email': user_admin_email,
        'otp': otp.otp
    })
    assert response.status_code == 204
    
    otp = OTP.get_by_user(user_admin)
    assert otp.last_successful_attempt is not None
    assert otp.num_attempts == 0

def test_update_password_no_body(client):
    response = client.post('/api/auth/password/update', json={})
    assert response.status_code == 422

def test_update_password_no_token(client):
    response = client.post('/api/auth/password/update', json={
        'old_password': '',
        'new_password': ''
    })
    assert response.status_code == 401
    
def test_update_password_invalid_password(client, user_admin, user_admin_token_header):
    response = client.post('/api/auth/password/update', headers=user_admin_token_header, json={
        'old_password': 'NotAPassword',
        'new_password': 'NotAPassword'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Current password is invalid'

def test_update_password(client, user_admin, user_admin_email, user_admin_password, user_admin_token_header):
    response = client.post('/api/auth/password/update', headers=user_admin_token_header, json={
        'old_password': user_admin_password,
        'new_password': 'NewPassword'
    })
    assert response.status_code == 204
    
    user = User.get_by_email(user_admin_email)
    assert check_password('NewPassword', user.password) is True

def test_lost_password_no_body(client):
    response = client.post('/api/auth/password/lost', json={})
    assert response.status_code == 422

def test_lost_password_invalid_email(client):
    response = client.post('/api/auth/password/lost', json={
        'email': 'nobody@gmail.com',
        'new_password': 'NotAPassword'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid email'

def test_lost_password(client, user_admin, user_admin_email):
    response = client.post('/api/auth/password/lost', json={
        'email': user_admin_email,
        'new_password': 'NewPassword'
    })
    assert response.status_code == 204
    
    user = User.get_by_email(user_admin_email)
    assert check_password('NewPassword', user.password) is True

def test_delete_account_no_token(client):
    response = client.delete('/api/auth/account')
    assert response.status_code == 401
    
def test_delete_account(client, user_admin_email, user_admin_token_header):
    response = client.delete('/api/auth/account', headers=user_admin_token_header)
    assert response.status_code == 204
    assert User.get_by_email(user_admin_email) is None