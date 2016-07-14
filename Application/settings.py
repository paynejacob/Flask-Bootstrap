# -*- coding: utf-8 -*-
"""
settings.py
Declares settings for the application
"""
import os
import sys

### logging configure values ###############################################
from logging import config

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'standard': {
      'format': '%(asctime)s| %(name)s/%(process)d: '
                '%(message)s @%(funcName)s:%(lineno)d #%(levelname)s',
    }
  },
  'handlers': {
    'console': {
      'formatter': 'standard',
      'class': 'logging.StreamHandler'
    },
  },
  'root': {
    'handlers': ['console'],
    'level': 'INFO',
  },
  'loggers': {
    'Application': {
      'level': 'INFO',
    },
  }
}
config.dictConfig(LOGGING)
############################################################################x

class Config():
  """
  Default config
  """
  APP_DIR = os.path.abspath(os.path.dirname(__file__))
  PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

  BCRYPT_LOG_ROUNDS = 13
  ASSETS_DEBUG = False
  ADMIN_ENABLED = True


class ProdConfig(Config):
  """Production configuration."""
  ENV = 'prod'
  DEBUG = False


class DevConfig(Config):
  """Development configuration."""
  ENV = 'dev'
  DEBUG = True

  # Uncomment this line to debug javascript/css assets
  # ASSETS_DEBUG = True
  SECRET_KEY = "dontprodme".encode("utf-8")

  DATABASE_NAME = 'my_apps_db'
  SQLALCHEMY_DATABASE_URI = 'sqlite:///'+DATABASE_NAME

  # Ease up on password requirements in dev to allow simple testing
  PASSWORD_REQUIRE_MIN = 4
  PASSWORD_REQUIRE_SPECIAL = False
  PASSWORD_REQUIRE_UPPER = False
  PASSWORD_REQUIRE_LOWER = False
  PASSWORD_REQUIRE_NUMBER = False

class TestConfig(Config):
  """
  Lite config for testing
  """
  TESTING = True
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'sqlite://'
  BCRYPT_LOG_ROUNDS = 1  # For faster tests
  WTF_CSRF_ENABLED = False  # Allows form testing
  ADMIN_ENABLED = False


def get_config_for_current_environment():
  """
  Checks environment variable, picks correct config
  """
  if len(sys.argv) > 1 and sys.argv[1] == 'test':
    return TestConfig
  elif os.environ.get("APP_ENV") == 'dev':
    return DevConfig
  else:
    # stage, demo, prod, etc. all get prod-like settings (e.g. no asset debugging)
    return ProdConfig
