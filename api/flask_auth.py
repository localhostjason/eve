from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

from . import app
from .models.user import User
from .errors import unauthorized, forbidden

token_auth = HTTPTokenAuth(scheme='Bearer')


@token_auth.verify_token
def verify_token(token):
    # print(token)
    if token:
        user = User.verify_auth_token(token)
        return user is not None
    return False


@token_auth.error_handler
def auth_error():
    return unauthorized('token过期或者不存在')
