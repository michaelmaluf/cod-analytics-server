import json

from flask import Blueprint, Response

from app.scraper.data_scraper import fetch_match_and_player_data
from app.services import MatchDataCoordinatorService
from app import db


scraper_bp = Blueprint('scraper', __name__, url_prefix='/scraper')

@scraper_bp.route('/run', methods=['GET'])
def scrape():
    scraped_data = fetch_match_and_player_data()
    coordinator_service = MatchDataCoordinatorService(db.session)
    coordinator_service.populate_all_data(scraped_data)
    return Response('Success', 200)
