def error_message(message, code=421):
    return {
        '_status': 'ERR',
        '_error': {
            'code': code,
            'message': message
        }
    }


def ok_message(kwargs=None):
    d = {
        '_status': 'OK',
    }
    if not kwargs:
        return d
    return dict(d, **kwargs)
