import jwt

from flask import Blueprint
from flask import current_app
from flask_apispec import use_kwargs, marshal_with, doc

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
    if not kwargs:
        error = {"message": "Please provide details"}
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
    if not kwargs:
        error = {"message": "Please provide details"}
        return error, 400
    try:
        user = User.get_by_email(kwargs.get('email'))
        if not user or not check_password(kwargs.get('password'), user.password):
            error = {"message": "Invalid email or password"}
            return error, 400
        try:
            user_token = jwt.encode(
                {"user_id": user.id},
                current_app.config["SECRET_KEY"],
                algorithm="HS256"
            )
            authenticated_user = {
                "user": user,
                "token": user_token
            }
            return authenticated_user, 200
        except Exception as e:
            error = {"message": str(e)}
            return error, 500
    except Exception as e:
        error = {"message": str(e)}
        return error, 400
    
def register_auth_api(application, docs):
    application.register_blueprint(auth_bp)
    docs.register(register, blueprint = auth_bp.name)
    docs.register(login, blueprint = auth_bp.name)

