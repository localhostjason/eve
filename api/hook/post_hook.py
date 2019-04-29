from .user import UserHook


class PostHook:
    @staticmethod
    def init_app(app):
        UserHook.init_post(app)
