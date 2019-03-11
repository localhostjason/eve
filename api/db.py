import datetime
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy_utils import force_instant_defaults


class BaseModel(Model):
    """
    :param
      enum_type: show enum name or value
      extra_kw : extra property value
      extra_dict: extra dict
      remove_key: del dict key
    @:return
      return new dict
    """

    def to_dict(self, extra_dict=None, remove_key=list()):
        model_field = [v for v in self.__dict__.keys() if not v.startswith('_') and v not in remove_key]
        result = dict()
        for info in model_field:
            result[info] = getattr(self, info)

        if extra_dict and isinstance(extra_dict, dict):
            for k, v in extra_dict.items():
                result[k] = v

        return result


'''
@force_instant_defaults

Function that assigns object column defaults on object initialization time.
By default calling this function applies instant defaults to all your models.
'''

force_instant_defaults()
db = SQLAlchemy(model_class=BaseModel)


class CommonColumns(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    _created = db.Column(db.DateTime, default=datetime.datetime.now)
    _updated = db.Column(db.DateTime, default=datetime.datetime.now)
    _etag = db.Column(db.String(40))


db.Model = CommonColumns
