from functools import wraps
from flask import render_template

def log_out(session):
    try:
        session.pop('username', None)
        session.pop('id', None)
        return True
    except:
        return False

# decorator:
def login_check(session):
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            template_name, result = func(*args, **kwargs)
            if session.get('id'):
                return render_template(template_name, **result, login=True)
            return render_template(template_name, **result)
        return inner
    return outer


