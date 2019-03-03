from eve import Eve
from eve.io.base import BaseJSONEncoder

from enum import Enum

from eve_sqlalchemy import SQL as _SQL
from eve_sqlalchemy.validation import ValidatorSQL

from settings import Settings
from .db import db


class MyEncoder(BaseJSONEncoder):
    """
    support enum.Enum, using keys
    """

    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name
        return super(MyEncoder, self).default(obj)


class SQL(_SQL):
    driver = db
    json_encoder_class = MyEncoder


settings = Settings().load_settings()


def create_app():
    app = Eve(validator=ValidatorSQL, data=SQL, settings=settings)
    print(app.config['STATIC_FOLDER'])
    app.static_folder = app.config['STATIC_FOLDER']
    db.init_app(app)

    return app
