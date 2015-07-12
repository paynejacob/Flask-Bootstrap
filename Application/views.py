# -*- coding: utf-8 -*-
"""Main UI section."""
from flask import Blueprint, Response, render_template, flash, url_for, redirect, request, current_app
from flask.ext.login import login_required, current_user

from . import utils

from Application.auth import role_required

blueprint = Blueprint('main', __name__, static_folder="../static")

###
### The UI application is driven by AngularJS, so a single server-driven
### template and a few helpers are all that is needed, in addition to the API.
###

@blueprint.route("/", methods=["GET"])
@login_required
def dashboard():
    context = {}
    return render_template("dashboard.html", **context)
