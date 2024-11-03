import time
import jwt
from app.config.config import settings
from app.internal.model.model import User


secret = settings.SECRET_KEY
algorithm = "HS256"


def generate_auth_token(user: User):
    token_expiry = int(time.time()) + settings.ACCESS_TOKEN_EXPIRE
    auth_token = jwt.encode(
        payload={
            "user_id": user.user_id,
            "email": user.email,
            "user_name": user.username,
            "token_expiry": token_expiry
        },
        key=secret,
        algorithm=algorithm
    )

    return auth_token


def __user_model(auth_token):
    user_model = jwt.decode(auth_token, secret, algorithm)
    return user_model


def valid_token(auth_token):
    user = __user_model(auth_token)
    time_now = int(time.time())
    if user['token_expiry'] >= time_now:
        return True
    return False
