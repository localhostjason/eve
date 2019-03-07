import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import force_instant_defaults

'''
@force_instant_defaults

Function that assigns object column defaults on object initialization time.
By default calling this function applies instant defaults to all your models.
'''

force_instant_defaults()
db = SQLAlchemy()


class CommonColumns(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    _created = db.Column(db.DateTime, default=datetime.datetime.now)
    _updated = db.Column(db.DateTime, default=datetime.datetime.now)
    _etag = db.Column(db.String(40))


db.Model = CommonColumns
