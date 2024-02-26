import os

class Config:
    DEBUG = False
    TESTING = False

class DevConfig(Config):
    FLASK_ENV = 'development'
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')
    DEBUG = True

class ProdConfig(Config):
    FLASK_ENV = 'production'
    SECRET_KEY = 'prod'
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URL')