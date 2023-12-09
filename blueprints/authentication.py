import jwt
import bcrypt

from flask import request
from flask import current_app
from flask import Blueprint

from models.user import User
from schemas.user import UserSchema

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    new_data = request.get_json()
    if not new_data:
        return {
            "message": "Please provide details",
        }, 400
    try:
        new_user = UserSchema().load(data=new_data)
        User.create(firstname=new_data["firstname"], surname=new_data["surname"], email=new_data["email"], password=User.encrypt_password(new_data["password"]))
        return {}, 201
    except Exception as e:
        return {
            "message": str(e)
        }, 400
    
@bp.route('/login', methods=['POST'])
def login():
    new_data = request.json
    if not new_data:
        return {
            "message": "Please provide details",
        }, 400
    try:
        user = User().login(new_data["email"], new_data["password"])
        if not user:
            return {
                "message:": "Invalid email or password"
            }, 400
        try:
            user_token = jwt.encode(
                {"user_id": user.id},
                current_app.config["SECRET_KEY"],
                algorithm="HS256"
            )
            print('login_OK3')
            return {
                "user": UserSchema().dump(user),
                "token": user_token
            }, 200
        except Exception as e:
            return {
                "message:": str(e)
            }, 500
    except Exception as e:
        return {
            "message:": str(e)
        }, 400    