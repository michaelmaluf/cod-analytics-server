import json

from flask import Blueprint, Response
from app.scraper.data_scraper import get_most_recent_match_date


scraper_bp = Blueprint('scraper', __name__, url_prefix='/scraper')

@scraper_bp.route('/run', methods=['GET'])
def scrape():
    get_most_recent_match_date()
    return Response('Success', 200)
