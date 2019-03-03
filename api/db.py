from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import force_instant_defaults

'''
@force_instant_defaults

Function that assigns object column defaults on object initialization time.
By default calling this function applies instant defaults to all your models.
'''

force_instant_defaults()
db = SQLAlchemy()
