# -*- coding: utf-8 -*-
"""
Admin module. Tees up the Flask-Admin blueprint.
"""
from flask_admin import AdminIndexView, Admin as WrappedAdmin
from flask_admin.contrib.sqla import ModelView

from .auth import current_user, AdminModels
from .database import db

class ProtectedModelView(ModelView):
  """
  Requires admin access to see model
  """
  def is_accessible(self):
    return current_user.is_admin


class ProtectedAdminIndexView(AdminIndexView):
  """
  Requires admin access to see index page
  """
  def is_accessible(self):
    return current_user.is_admin


class Admin():
  """
  Pretends to be the flask_admin.Admin object
  """
  def __init__(self):
    self.index_view = None
    self.admin = None

  def init_app(self, app):
    """
    Performs setup
    """
    self.index_view = ProtectedAdminIndexView(name='Admin Console')
    self.admin = WrappedAdmin(app, 'Application', index_view=self.index_view)
    for model in AdminModels:
      self.admin.add_view(ProtectedModelView(model, db.session))
