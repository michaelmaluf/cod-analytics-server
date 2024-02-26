import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import DevConfig, ProdConfig
from app.models import register_models

db = SQLAlchemy()

env_config = {
    'development': DevConfig,
    'production': ProdConfig
}

def create_app():
    app = Flask(__name__)

    config_class = env_config.get(os.getenv('FLASK_ENV', 'development'))
    app.config.from_object(config_class)
    db.init_app(app)

    with app.app_context():
        register_models()
        db.create_all()

    return app