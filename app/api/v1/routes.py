from flask import current_app
from flask_smorest import Api, Blueprint, abort

from app.schemas import PredictionResponseSchema, PredictionRequestSchema

predictions_bp = Blueprint('predictions', 'predictions', url_prefix='/predictions',
                           description='Endpoint for ML predictions')


@predictions_bp.route('', methods=['GET'])
@predictions_bp.arguments(PredictionRequestSchema, location='query')
@predictions_bp.response(200, PredictionResponseSchema)
def get_map_predictions(prediction_request):
    """
    Query map predictions by team_one, team_two, map, and game_mode.

    Returns the corresponding prediction scores for team_one and team_two.
    """
    return current_app.prediction_service.get_map_predictions(prediction_request)
    return 5
