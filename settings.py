from eve_sqlalchemy.config import DomainConfig, ResourceConfig
from api.models import *
from config import Config, MY_ROOT_DIR
import os


class Settings(Config):
    # SERVER_NAME = '0.0.0.0:6000'
    DEBUG = True
    EMBEDDING = True

    """
    @RESOURCE_METHODS 端点 支持http 方法 如: http://demo/user
    @ITEM_METHODS  端点 支持http 方法 如: http://demo/user/<id>
    """
    RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
    ITEM_METHODS = ['GET', 'PUT', 'PATCH', 'DELETE']

    URL_PREFIX = 'api'
    IF_MATCH = False  # disable etag from http://docs.python-eve.org/en/latest/features.html#concurrency
    X_DOMAINS = '*'
    X_HEADERS = '*'
    HATEOAS = False

    ALLOW_UNKNOWN = True  # for user.password_hash updated by password

    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    STATIC_FOLDER = os.path.join(MY_ROOT_DIR, 'static')

    DOMAIN = DomainConfig({
        'user': ResourceConfig(User),
        'role': ResourceConfig(Role),
        'address': ResourceConfig(Address),
    }).render()

    def load_settings(self):
        return {name: getattr(self, name) for name in dir(self) if
                not name.startswith('__') and not hasattr(getattr(self, name), '__call__')}
