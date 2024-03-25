from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.database import prepopulate_db

app = create_app()

with app.app_context():
    prepopulate_db()

if __name__ == '__main__':
    app.run()
