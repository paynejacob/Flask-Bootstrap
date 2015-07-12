import re
from flask_wtf import Form
from wtforms import TextField, PasswordField, ValidationError, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from flask import current_app
from flask.ext.login import current_user

from .models import User


def validate_password_complexity(form, field):
    """ Support configurable complexity requirements (with complex on by
        default) via the app's config (i.e. settings.py)
    """
    if not field.data or len(field.data) == 0:
        # Let `DataRequired` handle this case as necessary
        return

    min_length = current_app.config.get('PASSWORD_REQUIRE_MIN', 8)
    if min_length > 0:
        if len(field.data) < min_length:
            raise ValidationError('Password must be at least {} characters'.format(min_length))

    if current_app.config.get('PASSWORD_REQUIRE_SPECIAL', True):
        if not re.match(r'.*[^A-Za-z0-9]+', field.data):
            raise ValidationError('Password requires at least one special character')

    if current_app.config.get('PASSWORD_REQUIRE_UPPER', True):
        if not re.match(r'.*[A-Z]+', field.data):
            raise ValidationError('Password requires at least one upper case character')

    if current_app.config.get('PASSWORD_REQUIRE_LOWER', True):
        if not re.match(r'.*[a-z]+', field.data):
            raise ValidationError('Password requires at least one lower case character')

    if current_app.config.get('PASSWORD_REQUIRE_NUMBER', True):
        if not re.match(r'.*[0-9]+', field.data):
            raise ValidationError('Password requires at least one number')


class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user or not self.user.check_password(self.password.data):
            self.password.errors.append('Invalid username or password')
            return False

        if not self.user.active:
            self.username.errors.append('User account is not active')
            return False
        return True


class ChangePasswordForm(Form):
    old = PasswordField('Current Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired(),
                        EqualTo('confirm', message='Passwords must match'),
                        validate_password_complexity
                        ])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(ChangePasswordForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=current_user.username).first()
        if not self.user.check_password(self.old.data):
            self.password.errors.append('Invalid current password')
            return False

        return True


class CreateUserForm(Form):
    username = TextField('Username',
                    validators=[DataRequired(), Length(min=3, max=25)])
    full_name = TextField('Full name',
                    validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired(),
                        validate_password_complexity
                        ])
    confirm = PasswordField('Verify password',
                [DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(CreateUserForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        return True


class EditUserForm(Form):
    full_name = TextField('Full name',
                    validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[
                        validate_password_complexity
                        ])
    confirm = PasswordField('Verify password',
                [EqualTo('password', message='Passwords must match')])
    active = RadioField('Status', choices=[('True', 'Enabled'), ('False', 'Disabled')])
    is_admin = RadioField('Role', choices=[('True', 'Admin'), ('False', 'Basic')])
