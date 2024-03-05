from database.models.map_game_mode import GameMode
from app.enums import GameModeType
from database import db


def prepopulate_db():
    if not db.session.query(GameMode).first():

        for game_mode in GameModeType:
            game_mode_entry = GameMode(name=game_mode)
            db.session.add(game_mode_entry)

        db.session.commit()
        print('Database prepopulated with sample data.')
    else:
        print('Database already contains data; skipping prepopulation.')
