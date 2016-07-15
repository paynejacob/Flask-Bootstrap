#!/usr/bin/env python3
"""
manage.py
Scripts for running the applications
"""
import subprocess as sp


from flask_script import Manager, Shell, Server as OldServer
from flask_migrate import MigrateCommand, Migrate

from Application import create_app, db
from Application.settings import get_config_for_current_environment

from Application.auth.models import User

app = create_app(get_config_for_current_environment())
manager = Manager(app)
migrate = Migrate(app, db)

class Server(OldServer):

  def __call__(self, *args, **kwargs):
    webpack_server = sp.Popen(["/usr/bin/node",
                               "node_modules/webpack-dev-server/bin/webpack-dev-server.js",
                               "--inline",
                               "--hot",
                               "--port",
                               "8081"
                              ], cwd="Application/app_src")
    super().__call__(*args, **kwargs)

def _make_context():
  """Return context dict for a shell session so you can access
  app, db, and the User model by default.
  """
  return {'app': app, 'db': db, 'User': User}

@manager.command
def create_user():
  """Create a superuser"""
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

@manager.command
def npm_update():
  sp.run(["/usr/bin/npm", "update"], cwd="Application/app_src", check=True)

manager.add_command('runserver', Server(threaded=True))
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
  manager.run()
