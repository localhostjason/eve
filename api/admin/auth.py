from flask import request, jsonify
from .. import app
from api.models.user import User
from ..flask_auth import requires_auth


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

        role = None
        if user.role:
            role = user.role.to_dict()
        return jsonify({'success': True, 'errmsg': None, 'token': token, 'role': role})

    return jsonify({'success': False, 'errmsg': '用户名或者密码错误'})


@app.route('/api/admin/user_info', methods=['get'])
def get_admin_user_info():
    token = request.args.get('token')

    user = User.query.filter_by(token=token).first()
    print('start')
    if not user:
        return jsonify({'success': False, 'code': 401, 'errmsg': '没有用户或者token失效'})

    # print(user.to_dict())
    role = None
    if user.role:
        role = user.role.to_dict()
    return jsonify({'success': True, 'errmsg': None, 'user': user.to_dict(), 'role': role})


@app.route('/api/admin/logout', methods=['POST'])
@requires_auth
def admin_logout():
    req_data = request.get_json() or {}
    token = req_data.get('token')

    user = User.query.filter_by(token=token).first()
    if not user:
        return jsonify({'success': False, 'code': 401, 'errmsg': 'Token失效'})

    user.token = None
    return jsonify({'success': True, 'errmsg': None})
