#!/usr/bin/env python
from __future__ import print_function
import os
import sqlalchemy
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand, Migrate

from Application.settings import get_config_for_current_environment

from Application.app import create_app
from Application.auth.models import User
from Application.models import *
from Application.database import db

app = create_app(get_config_for_current_environment())
manager = Manager(app)
migrate = Migrate(app, db)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User}

@manager.command
def test():
    """Run the tests."""
    import pytest
    HERE = os.path.abspath(os.path.dirname(__file__))
    TEST_PATH = os.path.join(HERE, 'tests')
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code

@manager.command
def create_db():
    connection_string = app.config['SQLALCHEMY_DATABASE_URI']
    with sqlalchemy.create_engine(connection_string).connect() as connection:
        try:
            # connection.execute('CREATE DATABASE {}'.format(app.config['DATABASE_NAME']))
            print('Created database {}'.format(app.config['DATABASE_NAME']))
        except Exception as ex:
            # fails if db already exists
            print(ex.message)

@manager.command
def create_user():
    import getpass
    user = input("Username [{}]: ".format(getpass.getuser()))
    if not user:
        user = getpass.getuser()
    pprompt = lambda: (getpass.getpass(), getpass.getpass('Retype password: '))
    p1, p2 = pprompt()
    while p1 != p2:
        print('Passwords do not match. Try again')
        p1, p2 = pprompt()

    User.create(username=user, password=p1, active=True, is_admin=True)
    print('Administrator account created for {}'.format(user))


manager.add_command('server', Server(threaded=True))
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
