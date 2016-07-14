# -*- coding: utf-8 -*-
"""
views.py
Manages login views
"""
from functools import wraps
from flask import (Blueprint, request, render_template, flash, url_for,
                   redirect, abort)
from flask_login import (login_user, login_required, logout_user,
                         current_user)

from ..utils import flash_errors

from .login_manager import login_manager
from .forms import LoginForm, CreateUserForm, EditUserForm, ChangePasswordForm
from .models import User

blueprint = Blueprint("auth", __name__, url_prefix='/auth',
                      static_folder="../static")

login_manager.login_view = 'users.login'

@login_manager.unauthorized_handler
def unauthorized():
  """Try to make the user login"""
  if current_user and current_user.is_authenticated:
    return render_template('403.html')
  else:
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(uid):
  """Load users given string uid"""
  return User.query.get(int(uid))

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

@blueprint.route("/login/", methods=["GET", "POST"])
def login():
  """Log a user in"""
  form = LoginForm(request.form)
  if request.method == 'POST':
    if form.validate_on_submit():
      login_user(form.user)
      flash("You are logged in.", 'success')
      redirect_url = request.args.get("next") or url_for("main.dashboard")
      return redirect(redirect_url)
    else:
      flash_errors(form)
  return render_template("auth/login.html", form=form)

@blueprint.route('/logout/')
@login_required
def logout():
  logout_user()
  flash('You are logged out.', 'info')
  return redirect(url_for('auth.login'))

@blueprint.route("/change-password/", methods=["GET", "POST"])
@login_required
def change_password():
  form = ChangePasswordForm(request.form)
  if request.method == 'POST':
    if form.validate_on_submit():
      form.user.set_password(form.password.data)
      form.user.save()
      flash("Password successfully changed.", 'success')
      return redirect(url_for('auth.change_password'))
    else:
      flash_errors(form)
  return render_template("auth/change-password.html", form=form)

@blueprint.route('/users/')
@role_required('orgadmin')
def user_list():
  # User can only manage within their own organization
  users = (User.query
           .order_by(User.username)
           .all())
  return render_template("auth/user-list.html", users=users)

@blueprint.route("/users/add", methods=['GET', 'POST'])
@role_required('orgadmin')
def create_user():
  form = CreateUserForm(request.form)
  if form.validate_on_submit():
    new_user = User.create(username=form.username.data,
                           full_name=form.full_name.data,
                           password=form.password.data,
                           active=True)
    flash("'{username}' account created.".format(username=new_user.username), 'success')
    return redirect(url_for('auth.user_list'))
  else:
    flash_errors(form)
  return render_template('auth/user-add.html', form=form)

@blueprint.route("/users/<int:user_id>", methods=['GET', 'POST'])
@role_required('orgadmin')
def edit_user(user_id):
  user = User.query.filter_by(id=user_id).one()
  form = EditUserForm(request.form, user)
  if form.validate_on_submit():
    user.full_name = form.full_name.data
    if form.password.data:
      user.set_password(form.password.data)
    user.active = form.active.data == 'True'
    user.is_admin = form.is_admin.data == 'True'
    user.save()
    return redirect(url_for('auth.user_list'))
  else:
    flash_errors(form)
  return render_template('auth/user-edit.html', form=form, user=user)
