# -*- coding: utf-8 -*-
"""
models.py
"""
import datetime as dt

from flask_login import UserMixin
from . import crypto
from ..database import (Model, SurrogatePK, Column, db, ReferenceCol,
                        relationship)


class Role(SurrogatePK, Model):
  """
  A user's Role, allows them to perform certain actions
  """
  __tablename__ = 'roles'

  name = Column(db.String(80), unique=True, nullable=False)
  user_id = ReferenceCol('users', nullable=True)
  user = relationship('User', backref='roles')

  def __repr__(self):
    return '{name}'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
  """
  A user, capable of logging in and performing actions
  """
  __tablename__ = 'users'

  username = Column(db.String(80), unique=True, nullable=False)
  password = Column(db.String(128), nullable=True)
  salt = Column(db.String(128), nullable=True)
  full_name = Column(db.String(80), nullable=True)
  active = Column(db.Boolean(), default=False)
  is_admin = Column(db.Boolean(), default=False)
  created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

  def __init__(self, username=None, password=None, **kwargs):
    db.Model.__init__(self, username=username, **kwargs)
    if password:
      self.set_password(password)
    else:
      self.password = None

  def set_password(self, password):
    """Hashes and stores plaintext password"""
    self.salt = crypto.generate_random_salt()
    self.password = crypto.generate_password_hash(password, self.salt)

  def check_password(self, value):
    """Constant time check of password"""
    return crypto.check_password_hash(value, self.password, self.salt)

  def has_role(self, role, ignore_super=False):
    """
    Checks if user has a given role. Admins are assumed to have all roles.

    If *ignore_super* is not set to true,
    """
    if not ignore_super and self.is_admin:
      return True
    if role == "admin":
      return self.is_admin
    return any(str(role) == str(r) for r in self.roles)

  def to_json(self):
    """
    represents user as json object, omitting sensitive columns
    """
    return {
      'username': self.username,
      'fullName': self.full_name,
      'active': self.active
    }

  def __repr__(self):
    return '{username}'.format(username=self.username)

AdminModels = [Role, User]
