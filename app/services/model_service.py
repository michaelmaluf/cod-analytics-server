import joblib
from io import BytesIO

from sqlalchemy import desc

from app.database.models import MLModel, GameMode
from app.enums import GameModeType


class ModelService:
    def __init__(self, session):
        self.session = session
        self.HardpointModel = None
        self.SearchAndDestroyModel = None
        self.ControlModel = None
        self.fetch_models_from_database()


    def fetch_models_from_database(self):
        try:
            for game_mode in GameModeType:
                game_mode_model = self.session.query(GameMode, MLModel) \
                    .join(MLModel)\
                    .filter(GameMode.name == game_mode) \
                    .order_by(desc(MLModel.creation_date)) \
                    .first()[1]

                model_buffer = BytesIO(game_mode_model.model_data)

                if game_mode == GameModeType.HARDPOINT:
                    self.HardpointModel = joblib.load(model_buffer)
                elif game_mode == GameModeType.SEARCH_AND_DESTROY:
                    self.SearchAndDestroyModel = joblib.load(model_buffer)
                else:
                    self.ControlModel = joblib.load(model_buffer)
        except TypeError:
            print('ML Models table is empty, cannot load models.')