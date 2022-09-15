from flask import request, session
from util import generatedata, ERROR
from functools import wraps


def is_auth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return generatedata(ERROR, {},  'user not logged in'), 401
        return func(*args, **kwargs)
    return decorated_function


def is_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session['user'] != 'admin':
            return generatedata(ERROR, {},  'invalid access'), 401
        return func(*args, **kwargs)
    return decorated_function
