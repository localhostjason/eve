from .user import UserHook


class ExtraHook:
    @staticmethod
    def init_app(app):
        UserHook.init_extra(app)
