# ############################################
# import into create_app for access to 
# different configs, unfortunately must have
# path name when configuring as opposed to
# object class
# ###########################################

import os

# DEFAULT #
class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# PRODUCTION #
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

# DEVELOPMENT #
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or "sqlite:///app.db"

# TESTING #
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True