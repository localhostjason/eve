from flask import request, jsonify
from .. import app
from api.models.user import User
from ..flask_auth import token_auth
from api.common.message import *


@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    req_data = request.get_json()

    username = req_data.get('username')
    password = req_data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        token = user.generate_auth_token(expiration=36000).decode('ascii')
        user.token = token
        user.update_time_ip()

        role = user.role.to_dict() if user.role else {}
        return jsonify(ok_message({**user.to_dict(), **role}))

    return jsonify(error_message('用户名或者密码错误')), 421


@app.route('/api/admin/user_info', methods=['get'])
@token_auth.login_required
def get_admin_user_info():
    token = token_auth.get_auth()
    token = token.get('token')

    user = User.query.filter_by(token=token).first()
    if not user:
        return jsonify(error_message('没有用户或者token失效')), 421

    role = user.role.to_dict() if user.role else {}
    return jsonify(ok_message(ok_message({**user.to_dict(), **role})))


@app.route('/api/admin/logout', methods=['POST'])
@token_auth.login_required
def admin_logout():
    token = token_auth.get_auth()
    token = token.get('token')

    user = User.query.filter_by(token=token).first()
    if not user:
        return jsonify(error_message('Token失效')), 421

    user.token = None
    return jsonify(ok_message())
