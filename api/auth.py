import datetime

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import create_access_token, jwt_required, verify_jwt_in_request, current_user

from custom_exceptions import UserBlockedException
from shortcuts import check_password, encrypt_password

from data.models import User, OTP
from data.schemas import UserSchema, OTPSchema, LoginSchema, UserTokenSchema, UpdatePasswordSchema, ReinitPasswordSchema, ErrorSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
@use_kwargs(UserSchema, location='json')
@marshal_with(ErrorSchema, code=400)
@marshal_with(ErrorSchema, code=500)
@doc(description='Register new user', tags=['Auth'])
def register(**kwargs):
    if kwargs.get('is_superadmin') is True:
        error = {"message": "Superadmins cannot be created this way"}
        return error, 400
    if User.get_by_email(kwargs.get('email')):
        error = {"message": "Email already taken"}
        return error, 400
    try:
        User.create(**kwargs)
        return {}, 201
    except Exception as e:
        error = {"message": str(e)}
        return error, 500
    
@auth_bp.route('/login', methods=['POST'])
@use_kwargs(LoginSchema, location='json')
@marshal_with(UserTokenSchema, code=200)
@marshal_with(ErrorSchema, code=400)
@marshal_with(ErrorSchema, code=500)
@doc(description='Login user', tags=['Auth'])
def login(**kwargs):
    user = User.get_by_email(kwargs.get('email'))
    if not user or not check_password(kwargs.get('password'), user.password):
        error = {"message": "Invalid email or password"}
        return error, 400
    otp = OTP.get_by_user(user)
    if otp.is_blocked:
        error = {"message": "User is blocked"}
        return error, 500
    if not otp.is_still_valid:
        error = {"message": "Need to revalidate OTP"}
        return error, 500
    try:
        authenticated_user = {
            "user": user,
            "token": create_access_token(identity=user)
        }
        return authenticated_user, 200
    except Exception as e:
        error = {"message": str(e)}
        return error, 500
    
@auth_bp.route('/otp/send', methods=['POST'])
@use_kwargs(LoginSchema, location='json')
@marshal_with(OTPSchema, code=201)
@marshal_with(ErrorSchema, code=400)
@marshal_with(ErrorSchema, code=500)
@doc(description='Send OTP for user', tags=['Auth'])
def send_otp(**kwargs):
    user = User.get_by_email(kwargs.get('email'))
    if not user:
        error = {"message": "Invalid email or password"}
        return error, 400
    if kwargs.get('password') and not (check_password(kwargs.get('password'), user.password)):
        error = {"message": "Invalid email or password"}
        return error, 400
    otp = OTP.get_by_user(user)
    if otp and otp.is_blocked:
        error = {"message": "User is blocked"}
        return error, 500
    
    try:
        otp = OTP.create_or_update_otp(user)
        generated_otp = {
            "otp": otp.otp,
            "email": user.email,
        }
        return generated_otp, 201
    except UserBlockedException as e:
        error = {"message": str(e)}
        return error, 500

@auth_bp.route('/otp/validate', methods=['POST'])
@use_kwargs(OTPSchema, location='json')
@marshal_with(UserTokenSchema, code=200)
@marshal_with(ErrorSchema, code=400)
@marshal_with(ErrorSchema, code=500)
@doc(description='Validate OTP for user', tags=['Auth'])
def validate_otp(**kwargs):
    user = User.get_by_email(kwargs.get('email'))
    if not user:
        error = {"message": "Invalid email or password"}
        return error, 400
    if kwargs.get('password') and not (check_password(kwargs.get('password'), user.password)):
        error = {"message": "Invalid email or password"}
        return error, 400
    otp = OTP.get_by_user(user)
    if not otp:
        error = {"message": "OTP not found"}
        return error, 500
    if otp.is_blocked:
        error = {"message": "User is blocked"}
        return error, 500
    if not otp.otp == kwargs.get('otp'):
        error = {"message": "OTP challenge failed"}
        return error, 400
    
    otp.last_successful_attempt = datetime.datetime.now()
    otp.blocked_since = None
    otp.num_attempts = 0
    otp.save()
    
    if kwargs.get('password'):
        try:
            authenticated_user = {
                "user": user,
                "token": create_access_token(identity=user)
            }
            return authenticated_user, 200
        except Exception as e:
            error = {"message": str(e)}
            return error, 500
    else:
        return {}, 204

@jwt_required()
@auth_bp.route('/password/update', methods=['POST'])
@use_kwargs(UpdatePasswordSchema, location='json')
@marshal_with(ErrorSchema, code=400)
@marshal_with(ErrorSchema, code=500)
def update_password(**kwargs):
    if verify_jwt_in_request():
        if not check_password(kwargs.get('old_password'), current_user.password):
            error = {"message": "Current password is invalid"}
            return error, 400
        current_user.password = encrypt_password(kwargs.get('new_password'))
        current_user.save()
        return {}, 204

@auth_bp.route('/password/lost', methods=['POST'])
@use_kwargs(ReinitPasswordSchema, location='json')
@marshal_with(ErrorSchema, code=400)
@marshal_with(ErrorSchema, code=500)
def lost_password(**kwargs):
    user = User.get_by_email(kwargs.get('email'))
    if not user:
        error = {"message": "Invalid email"}
        return error, 400
    user.password = encrypt_password(kwargs.get('new_password'))
    user.save()
    return {}, 204

@jwt_required()
@auth_bp.route('/account', methods=['DELETE'])
@marshal_with(ErrorSchema, code=400)
@marshal_with(ErrorSchema, code=500)
@doc(description='Delete user account', tags=['Auth'])
def delete_account():
    if verify_jwt_in_request():
        try:
            current_user.delete_instance(recursive=True)
            return {}, 204
        except Exception as e:
            error = {"message": str(e)}
            return error, 500
        

def register_auth_api(application, docs):
    application.register_blueprint(auth_bp)
    docs.register(register, blueprint = auth_bp.name)
    docs.register(login, blueprint = auth_bp.name)
    docs.register(send_otp, blueprint = auth_bp.name)
    docs.register(validate_otp, blueprint = auth_bp.name)
    docs.register(update_password, blueprint = auth_bp.name)
    docs.register(lost_password, blueprint = auth_bp.name)
    docs.register(delete_account, blueprint = auth_bp.name)
    

