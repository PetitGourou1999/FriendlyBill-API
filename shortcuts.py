import bcrypt

def encrypt_password(clear_text_password):
    hashed_password = bcrypt.hashpw(bytes(clear_text_password, 'utf-8'), bcrypt.gensalt())
    return hashed_password.decode()

def check_password(clear_text_password, hashed_password):
    return bcrypt.hashpw(bytes(clear_text_password, 'utf-8'), bytes(hashed_password, 'utf-8')) == bytes(hashed_password, 'utf-8')