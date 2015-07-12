# -*- coding: utf-8 -*-
"""Admin module. Tees up the Flask-SuperAdmin blueprint.
"""
import logging

from flask import render_template
from flask.ext.login import current_user
from flask.ext.superadmin import AdminIndexView, Admin as SuperAdmin
from flask.ext.superadmin.model import ModelAdmin
from Application import models
from Application.extensions import db


class ProtectedModelView(ModelAdmin):

    session = db.session

    def is_accessible(self):
        return role_required('admin').has_role()


class ProtectedAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_admin


class Admin(object):

    def init_app(self, app):
        index_view = ProtectedAdminIndexView(name='Admin Console')
        admin = SuperAdmin(app, 'Application', index_view=index_view)

        admin.register(models.User, ProtectedModelView)
