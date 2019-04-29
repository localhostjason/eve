from flask_cors import CORS
from eve import Eve
from eve.io.base import BaseJSONEncoder
from eve.auth import TokenAuth

from enum import Enum

from eve_sqlalchemy import SQL as _SQL
from eve_sqlalchemy.validation import ValidatorSQL

from settings import Settings
from .db import db
from .models.user import User

from .hook.pre_hook import PreHook
from .hook.extra_hook import ExtraHook
from .hook.post_hook import PostHook


class MYAuth(TokenAuth):
    """
    token auth
    """

    def check_auth(self, token, allowed_roles, resource, method):
        """For the purpose of this example the implementation is as simple as
        possible. A 'real' token should probably contain a hash of the
        username/password combo, which sould then validated against the account
        data stored on the DB.
        """
        user = User.verify_auth_token(token)

        user_token = User.query.get(user.id if user else 0)
        if user is not None:
            self.set_request_auth_value(user)
        return user_token and user_token.token


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
    app = Eve(validator=ValidatorSQL, data=SQL, settings=settings, auth=MYAuth)
    CORS(app)
    # print(app.config['STATIC_FOLDER'])
    app.static_folder = app.config['STATIC_FOLDER']
    db.init_app(app)

    ExtraHook.init_app(app)
    PreHook.init_app(app)
    PostHook.init_app(app)

    return app
