"""
Application.__init__.py
A skeleton for a modern webapp
"""
from . import (admin, app, assets, auth, database, models,
               settings, views, utils)

create_app = app.create_app
db = database.db
