from eve_sqlalchemy.config import DomainConfig, ResourceConfig
from api.domain import *
from config import Config


class Settings(Config):
    SERVER_NAME = '192.168.120.244:5000'
    RESOURCE_METHODS = ['GET', 'POST']

    DOMAIN = DomainConfig({
        'parents': ResourceConfig(Parent),
        'children': ResourceConfig(Child)
    }).render()

    def load_settings(self):
        return {name: getattr(self, name) for name in dir(self) if
                not name.startswith('__') and not hasattr(getattr(self, name), '__call__')}


if __name__ == '__main__':
    Settings().load_settings()
