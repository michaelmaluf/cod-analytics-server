import os

from flask import Flask

from app.config import DevConfig, ProdConfig
from database import db
# from database.models import register_models
from database.models import *

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
        # register_models()
        # db.drop_all()
        db.create_all()

    from app.api import scraper_bp
    app.register_blueprint(scraper_bp)

    return app