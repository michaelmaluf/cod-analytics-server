from app.models.game_mode import GameMode
from app.enums import GameModeType
from app import db

def prepopulate_db():
    if not GameMode.query.first():

        for game_mode in GameModeType:
            game_mode_entry = GameMode(name=game_mode)
            db.session.add(game_mode_entry)

        db.session.commit()
        print('Database prepopulated with sample data.')
    else:
        print('Database already contains data; skipping prepopulation.')