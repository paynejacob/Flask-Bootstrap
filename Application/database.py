# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related
utilities.
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()
# Alias common SQLAlchemy names
Column = db.Column
relationship = relationship

class CRUDMixin():
  """
  Mixin that adds convenience methods for CRUD (create, read, update, delete)
  operations.
  """

  @classmethod
  def create(cls, **kwargs):
    """Create a new record and save it the database."""
    instance = cls(**kwargs)
    return instance.save()

  def update(self, commit=True, **kwargs):
    """Update specific fields of a record. Chainable"""
    for attr, value in kwargs:
      setattr(self, attr, value)
    return self.save(commit=commit)

  def save(self, commit=True):
    """Save the record. Chainable"""
    db.session.add(self)
    if commit:
      self.commit()
    return self

  def delete(self, commit=True):
    """Remove the record from the database."""
    db.session.delete(self)
    if commit:
      self.commit()

  def commit(self):
    """Do a commit. May be unnecessary"""
    try:
      db.session.commit()
    except:
      db.session.rollback()
      db.session.flush()
      raise

class Model(CRUDMixin, db.Model):
  """Base model class that includes CRUD convenience methods."""
  __abstract__ = True

# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK():
  """A mixin that adds a surrogate integer 'primary key' column named
  ``id`` to any declarative-mapped class.
  """
  __table_args__ = {'extend_existing': True}

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

def ReferenceCol(tablename, nullable=False, pk_name='id', **kwargs):
  """Column that adds primary key foreign key reference.

  Usage: ::

    category_id = ReferenceCol('category')
    category = relationship('Category', backref='categories')
  """
  return db.Column(
    db.ForeignKey("{0}.{1}".format(tablename, pk_name)),
    nullable=nullable, **kwargs)
