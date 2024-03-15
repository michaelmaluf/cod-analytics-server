import os

class Config:
    DEBUG = False
    TESTING = False
    API_TITLE = 'COD API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'


class DevConfig(Config):
    FLASK_ENV = 'development'
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')
    DEBUG = True
    OPENAPI_JSON_PATH = 'openapi.json'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_SWAGGER_UI_PATH = '/swagger-ui'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'


class ProdConfig(Config):
    FLASK_ENV = 'production'
    SECRET_KEY = 'prod'
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URL')