from flask import request, jsonify
from .. import app, db
from api.models.user import User
from ..flask_auth import requires_auth


@app.route('/api/register', methods=['POST'])
def register():
    req_data = request.get_json() or {}

    phone = req_data.get('phone')
    password = req_data.get('password')

    if not phone or not password:
        return jsonify({'success': False, 'errmsg': '用户名或者密码不能为空'})

    old_user = User.query.filter_by(phone=phone).first()
    if old_user:
        return jsonify({'success': False, 'errmsg': '用户名已存在'})

    user = User(phone=phone, password=password)
    db.session.add(user)
    return jsonify({'success': True, 'errmsg': None})


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
        return jsonify({'success': True, 'errmsg': None, 'token': token})

    return jsonify({'success': False, 'errmsg': '用户名或者密码错误'})


@app.route('/api/user_info', methods=['get'])
def get_user_info():
    token = request.args.get('token')

    user = User.query.filter_by(token=token).first()
    if not user:
        return jsonify({'success': False, 'errmsg': '没有用户或者token失效'})

    return jsonify({'success': True, 'errmsg': None, 'data': user.to_dict()})


@app.route('/api/logout', methods=['POST'])
@requires_auth
def logout():
    req_data = request.get_json() or {}
    token = req_data.get('token')

    user = User.query.filter_by(token=token).first()
    if not user:
        return jsonify({'success': False, 'errmsg': 'Token失效'})

    user.token = None
    return jsonify({'success': True, 'errmsg': None})
