from api.models.user import *


def insert_admin():
    admin = User(username='admin')
    admin.password = '123'
    db.session.add(admin)
    db.session.commit()
