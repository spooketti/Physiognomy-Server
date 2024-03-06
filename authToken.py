from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from model.users import Users

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("jwt")
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Missing Token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user=Users.query.filter_by(userID=data["userID"]).first() 
            if current_user is None:
                return {
                "message": "Invalid Token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            print(e)
            return {
                "message": "An Exception has occurred",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)


    return decorated