from .post import *
from .extra import *
from .pre import *


class UserHook:
    @staticmethod
    def init_extra(app):
        pass

    @staticmethod
    def init_post(app):
        pass

    @staticmethod
    def init_pre(app):
        pass
