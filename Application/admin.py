# -*- coding: utf-8 -*-
"""Admin module. Tees up the Flask-Admin blueprint.
"""
from flask import render_template
from flask.ext.login import current_user
from flask.ext.admin import AdminIndexView, Admin as WrappedAdmin
from flask.ext.admin.contrib.sqla import ModelView

from Application.auth import role_required, AdminModels
from Application.extensions import db



class ProtectedModelView(ModelView):

    def is_accessible(self):
        return role_required('admin').has_role()


class ProtectedAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return role_required('admin').has_role()


class Admin(object):

    def init_app(self, app):
        from Application.auth import models as auth_models
        index_view = ProtectedAdminIndexView(name='Admin Console')
        admin = WrappedAdmin(app, 'Application', index_view=index_view, template_mode="bootstrap3")
        for model in AdminModels:
            admin.add_view(ProtectedModelView(model, db.session))
