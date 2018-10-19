from eve import Eve
from eve_sqlalchemy import SQL as _SQL
from eve_sqlalchemy.validation import ValidatorSQL

from settings import Settings
from .db import db


class SQL(_SQL):
    driver = db


settings = Settings().load_settings()


def create_app():
    app = Eve(validator=ValidatorSQL, data=SQL, settings=settings)
    db.init_app(app)

    return app
