from flask import redirect
from .. import app, db
from api.models.domain import User


@app.route('/')
def index():
    user = User.query.filter_by(username='admin').first()
    token = user.generate_auth_token(expiration=3600)

    user.token = token
    db.session.add(user)
    print(token)
    return redirect('/static/index.html')
