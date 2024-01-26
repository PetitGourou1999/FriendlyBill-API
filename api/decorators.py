import jwt

from functools import wraps

from flask import request, abort
from flask import current_app

from data.models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
            }, 401
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.get_or_none(User.id == data["user_id"])
            if current_user is None:
                return {
                    "message": "Invalid Authentication token!",
                }, 401
            #if not current_user["active"]:
            #    abort(403)
        except Exception as e:
            return {
                "message": str(e),
            }, 500

        return f(*args, **kwargs)

    return decorated
