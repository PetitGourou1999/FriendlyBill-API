from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import create_access_token, jwt_required, verify_jwt_in_request, current_user

from shortcuts import check_password

from data.models import User
from data.schemas import UserSchema, LoginSchema, UserTokenSchema, ErrorSchema

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
    try:
        user = User.get_by_email(kwargs.get('email'))
        if not user or not check_password(kwargs.get('password'), user.password):
            error = {"message": "Invalid email or password"}
            return error, 400
        try:
            authenticated_user = {
                "user": user,
                "token": create_access_token(identity=user)
            }
            return authenticated_user, 200
        except Exception as e:
            error = {"message": str(e)}
            return error, 500
    except Exception as e:
        error = {"message": str(e)}
        return error, 400

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
    docs.register(delete_account, blueprint = auth_bp.name)

