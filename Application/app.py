# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template, got_request_exception

from Application.assets import assets
from Application.extensions import (
    bcrypt, db, login_manager, migrate, admin
)
from Application import views, models
from Application.auth import views as auth_views

from Application.settings import ProdConfig

def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    if (app.config['ADMIN_ENABLED']):
        register_admin_interface(app)

    return app

def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

def register_admin_interface(app):
    admin.init_app(app)

def register_blueprints(app):
    app.register_blueprint(views.blueprint)
    app.register_blueprint(auth_views.blueprint)

def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
