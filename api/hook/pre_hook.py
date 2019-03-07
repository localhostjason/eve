import json


# delete时候带的where有bug，自己添加一个才有用
# from https://stackoverflow.com/questions/43268784/python-eve-conditional-bulk-delete

def add_delete_filters(resource, request, lookup):
    if 'where' in request.args:
        conditions = request.args.getlist('where')
        for cond_str in conditions:
            cond = json.loads(cond_str)
            for attrib in cond:
                lookup[attrib] = cond[attrib]


class PreHook:
    @staticmethod
    def init_app(app):
        app.on_pre_DELETE += add_delete_filters