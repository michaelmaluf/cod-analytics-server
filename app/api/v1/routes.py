from flask import current_app
from flask_smorest import Blueprint

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
    predictions = current_app.prediction_service.get_map_predictions(prediction_request)
    return predictions


scraper_bp = Blueprint('scraper', __name__, url_prefix='/scraper', description='Endpoint for activating the data scraper')

@scraper_bp.route('/run', methods=['GET'])
@scraper_bp.response(204)
def scrape():
    """
    Calls the data scraper to fetch new data and populate the database with the new data made available.
    """
    current_app.competitive_data_sync_service.populate_all_data()
    return '', 204