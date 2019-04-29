import json
from flask import current_app, abort
from .user import UserHook


# delete时候带的where有bug，自己添加一个才有用
# from https://stackoverflow.com/questions/43268784/python-eve-conditional-bulk-delete

def add_delete_filters(resource, request, lookup):
    if 'where' in request.args:
        conditions = request.args.getlist('where')
        for cond_str in conditions:
            cond = json.loads(cond_str)
            for attrib in cond:
                lookup[attrib] = cond[attrib]


# 权限控制
def user_restricted_lookup(resource):
    user = current_app.auth.get_request_auth_value()
    # 获得真正的用户
    if resource in ['role']:
        return {}

    if resource == 'user':
        return {'id': user.id}

    # return {'user_id': user.id}
    return {}


def pre_GET(resource, request, lookup):
    lookup.update(user_restricted_lookup(resource))


def pre_POST(resource, request):
    print(resource, request)


def pre_PATCH(resource, request, lookup):
    lookup.update(user_restricted_lookup(resource))


def pre_DELETE(resource, request, lookup):
    lookup.update(user_restricted_lookup(resource))
    add_delete_filters(resource, request, lookup)


class PreHook:
    @staticmethod
    def init_app(app):
        app.on_pre_DELETE += add_delete_filters

        app.on_pre_GET += pre_GET
        app.on_pre_POST += pre_POST
        app.on_pre_PATCH += pre_PATCH
        app.on_pre_DELETE += pre_DELETE

        UserHook.init_pre(app)
