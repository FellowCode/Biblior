from functools import wraps
from threading import Thread


def make_async(func, hook):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper