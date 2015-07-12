# -*- coding: utf-8 -*-
import re

from flask import (abort, Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import (login_user, login_required, logout_user,
                    current_user)

from Application.extensions import login_manager
from Application.utils import flash_errors
from Application.database import db

from . import role_required
from .forms import LoginForm, CreateUserForm, EditUserForm, ChangePasswordForm
from .models import User, Role

blueprint = Blueprint("auth", __name__, url_prefix='/auth',
                        static_folder="../static")

login_manager.login_view = 'users.login'

@login_manager.unauthorized_handler
def unauthorized():
    if current_user and current_user.is_authenticated():
        return render_template('401.html')
    else:
        return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))

@blueprint.route("/login/", methods=["GET", "POST"])
def login():
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
        flash("'{username}' account created.".format(username=form.username.data), 'success')
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
        user.active = form.active.data == u'True'
        user.is_admin = form.is_admin.data == u'True'
        user.save()
        return redirect(url_for('auth.user_list'))
    else:
        flash_errors(form)
    return render_template('auth/user-edit.html', form=form, user=user)
