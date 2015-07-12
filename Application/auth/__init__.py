"""The user module."""

from flask import render_template, make_response
from flask.ext.login import current_user
from functools import wraps


class role_required(object):
    """ Decorator that will verify the user has the specified role """

    def __init__(self, role):
        self.role = role

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            if self.has_role():
                return func(*args, **kwargs)
            else:
                return self.handle_error()
        return decorated

    def has_role(self):
        return hasattr(current_user, 'has_role') and current_user.has_role(self.role)

    def handle_error(self):
        return make_response(render_template('401.html'), 401)
