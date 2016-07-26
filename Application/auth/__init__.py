"""
auth.__init__.py
Handles authorization for users and admins
"""
from flask_login import current_user
import flask_scrypt as crypto

from . import (forms, models, views)
from .models import AdminModels
from .views import role_required
from .login_manager import login_manager

__all__ = ["role_required", "AdminModels", "current_user",
           "login_manager", "crypto", "forms", "models", "views"]
