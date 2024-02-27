from .chrome_driver import ChromeDriver
from app import db
from app.models.match import Match

chrome_driver = ChromeDriver()


def get_most_recent_match_date():
    most_recent = db.session.query(db.func.max(Match.date)).scalar()
    print(most_recent)
    print(chrome_driver.get_webpage('https://google.com'))


