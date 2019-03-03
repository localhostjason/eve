from eve_sqlalchemy.config import DomainConfig, ResourceConfig
from api.models.domain import *
from config import Config, MY_ROOT_DIR


class Settings(Config):
    # SERVER_NAME = '0.0.0.0:6000'

    """
    @RESOURCE_METHODS 端点 支持http 方法 如: http://demo/user
    @ITEM_METHODS  端点 支持http 方法 如: http://demo/user/<id>
    """
    RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
    ITEM_METHODS = ['GET', 'PUT', 'PATCH', 'DELETE']

    URL_PREFIX = 'api'

    DOMAIN = DomainConfig({
        'parents': ResourceConfig(Parent),
        'children': ResourceConfig(Child)
    }).render()

    def load_settings(self):
        return {name: getattr(self, name) for name in dir(self) if
                not name.startswith('__') and not hasattr(getattr(self, name), '__call__')}


if __name__ == '__main__':
    Settings().load_settings()
