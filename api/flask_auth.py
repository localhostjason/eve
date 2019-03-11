from .models.user import User
from flask import request, jsonify, Response, abort
from functools import wraps
from werkzeug.http import parse_authorization_header


def check_auth(token):
    user = User.verify_auth_token(token)
    if user is not None:
        return True
    return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic Token="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        try:
            auth_token = auth_header.split(" ")[1]
        except Exception as e:
            print(e)
            auth_token = ''

        if not auth_token or not check_auth(auth_token):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def get_current_uid():
    auth_header = request.headers.get('Authorization')
    try:
        auth_token = auth_header.split(" ")[1]
    except Exception as e:
        print(e)
        auth_token = ''

    user = User.verify_auth_token(auth_token)
    return user.id if user else None


def check_uid(uid):
    if uid is None:
        abort(404, 'unknown user')
