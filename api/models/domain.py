from ..db import db
from werkzeug.security import generate_password_hash, check_password_hash


class Parent(db.Model):
    name = db.Column(db.String(100))


class Child(db.Model):
    name = db.Column(db.String(100))


class User(db.Model):
    username = db.Column(db.String(64))
    _password = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password not readable')

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)
