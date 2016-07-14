"""
auth.__init__.py
Handles authorization for users and admins
"""
from functools import wraps
from flask import render_template, abort
from flask_login import current_user, LoginManager
import flask_scrypt as crypto

from . import (forms, models, views)
from .models import AdminModels

login_manager = LoginManager()

def role_required(role):
  """ Fails requests if the user does not have the specified role """
  def wrapper(wrapped):
    """enforces role_required"""
    @wraps(wrapped)
    def f(*args, **kwargs):
      """dummy wrapped function"""
      if current_user.has_role(role):
        return wrapped(*args, **kwargs)
      else:
        abort(403)
    return f
  return wrapper

__all__ = ["role_required", "AdminModels", "current_user", "login_manager"]
