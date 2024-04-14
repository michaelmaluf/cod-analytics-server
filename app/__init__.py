import os
import logging

from flask import Flask
from flask_migrate import Migrate
from flask_smorest import Api
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

from app.config import DevConfig, ProdConfig
from app.database import db, prepopulate_db

env_config = {
    'development': DevConfig,
    'production': ProdConfig
}

def create_app():
    app = Flask(__name__)
    CORS(app)
    config_class = env_config.get(os.getenv('FLASK_ENV', 'development'))
    app.config.from_object(config_class)
    db.init_app(app)

    logging.basicConfig()
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    migrate = Migrate(app, db)

    api = Api(app)

    with app.app_context():
        from app.services import PredictionService, CompetitiveDataSyncService, RosterService
        prepopulate_db()
        app.prediction_service = PredictionService(session=db.session)
        app.competitive_data_sync_service = CompetitiveDataSyncService(session=db.session)
        app.roster_service = RosterService(session=db.session)

    from app.api import scraper_bp, predictions_bp, rosters_bp
    api.register_blueprint(scraper_bp)
    api.register_blueprint(predictions_bp)
    api.register_blueprint(rosters_bp)

    return app