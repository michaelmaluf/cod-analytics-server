from dotenv import load_dotenv

load_dotenv()

from app import create_app, db
from machine_learning.training import train_all_models, perform_grid_search_all_models


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        train_all_models(db.session)
        perform_grid_search_all_models(db.session)