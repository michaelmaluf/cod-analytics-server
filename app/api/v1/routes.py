import os

from flask import current_app, request, jsonify
from flask_smorest import Blueprint

from app import db
from app.schemas import PredictionResponseSchema, PredictionRequestSchema, PlayersByTeamRequestSchema, PlayersByTeamResponseSchema
from machine_learning.training import train_all_models

predictions_bp = Blueprint('predictions', 'predictions', url_prefix='/predictions',
                           description='Endpoint for ML predictions')

rosters_bp = Blueprint('rosters', 'rosters', url_prefix='/rosters',
                           description='Endpoint for rosters (teams and players)')

scraper_bp = Blueprint('scraper', __name__, url_prefix='/scraper', description='Endpoint for activating the data scraper')


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

@rosters_bp.route('/all', methods=['GET'])
def get_all_rosters():
    """
    Get players for all 12 rosters.

    """
    rosters = current_app.roster_service.get_all_rosters()
    return jsonify(rosters), 200


@rosters_bp.route('', methods=['GET'])
@rosters_bp.arguments(PlayersByTeamRequestSchema, location='query')
@rosters_bp.response(200, PlayersByTeamResponseSchema)
def get_players_by_team(team_name_request):
    """
    Query the 4 active players given a team name.

    """
    team_name = team_name_request['team_name']
    players = {'players': current_app.roster_service.find_player_names_by_team_name(team_name)}
    return PlayersByTeamResponseSchema().dump(players)



@scraper_bp.route('/run', methods=['GET'])
@scraper_bp.response(200)
def scrape():
    """
    Calls the data scraper to fetch new data and populate the database with the new data made available.
    """
    # current_app.competitive_data_sync_service.populate_all_data()
    current_app.competitive_data_sync_service.update_player_rankings_for_game_modes()
    # train_all_models(db.session)
    return 'Scraper successfully ran, db updated with new data, ML models updated to reflect new data', 200

@scraper_bp.before_request
def before_request_func():
    if request.headers.get('X-API-Key') != os.getenv('X-API-KEY'):
        return 'Unauthorized Access', 401