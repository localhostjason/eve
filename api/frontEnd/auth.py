from flask import request, jsonify
from .. import app, db
from api.models.user import User
from ..flask_auth import token_auth
from api.common.message import *


@app.route('/api/register', methods=['POST'])
def register():
    req_data = request.get_json() or {}

    phone = req_data.get('phone')
    password = req_data.get('password')

    if not phone or not password:
        return jsonify(error_message('用户名或者密码不能为空')), 421

    old_user = User.query.filter_by(phone=phone).first()
    if old_user:
        return jsonify(error_message('用户名已存在')), 421

    user = User(phone=phone, password=password)
    db.session.add(user)
    return jsonify(ok_message())


@app.route('/api/login', methods=['POST'])
def login():
    req_data = request.get_json()

    phone = req_data.get('phone')
    password = req_data.get('password')

    user = User.query.filter_by(phone=phone).first()
    if user and user.verify_password(password):
        token = user.generate_auth_token(expiration=36000).decode('ascii')
        user.token = token
        user.update_time_ip()
        return jsonify(ok_message(user.to_dict()))

    return jsonify(error_message('用户名或者密码错误')), 421


@app.route('/api/logout', methods=['POST'])
@token_auth.login_required
def logout():
    token = token_auth.get_auth()
    token = token.get('token')

    user = User.query.filter_by(token=token).first()
    if not user:
        return jsonify(error_message('Token失效')), 421

    user.token = None
    return jsonify(ok_message())
