from flask import request, jsonify
from .. import app
from api.models.user import User
from ..flask_auth import requires_auth


@app.route('/api/login', methods=['POST'])
def login():
    req_data = request.get_json()

    username = req_data.get('username')
    password = req_data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        token = user.generate_auth_token(expiration=3600).decode('ascii')
        user.token = token
        user.update_time_ip()
        return jsonify({'success': True, 'errmsg': None, 'token': token})

    return jsonify({'success': False, 'errmsg': '用户名或者密码错误'})


@app.route('/api/user_info', methods=['get'])
def get_user_info():
    token = request.args.get('token')

    user = User.query.filter_by(token=token).first_or_404()
    return jsonify({'success': True, 'errmsg': None, 'data': user.to_dict()})


@app.route('/api/logout', methods=['POST'])
@requires_auth
def logout():
    req_data = request.get_json() or {}
    token = req_data.get('token')

    user = User.query.filter_by(token=token).first_or_404()
    user.token = None
    return jsonify({'success': True, 'errmsg': None})
