class Config(object):
    TESTING = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = '????'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
