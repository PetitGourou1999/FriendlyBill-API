import bcrypt
import datetime
import random
import string

def encrypt_password(clear_text_password):
    hashed_password = bcrypt.hashpw(bytes(clear_text_password, 'utf-8'), bcrypt.gensalt())
    return hashed_password.decode()

def check_password(clear_text_password, hashed_password):
    return bcrypt.hashpw(bytes(clear_text_password, 'utf-8'), bytes(hashed_password, 'utf-8')) == bytes(hashed_password, 'utf-8')

def generate_otp(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))