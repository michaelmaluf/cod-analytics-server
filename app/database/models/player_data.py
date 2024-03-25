from sqlalchemy.dialects.postgresql import UUID

from app.database import db

class PlayerData(db.Model):
    __tablename__ = 'player_data'
    match_map_id = db.Column(UUID(as_uuid=True), db.ForeignKey('match_maps.id'), primary_key=True)
    player_id = db.Column(UUID(as_uuid=True), db.ForeignKey('players.id'), primary_key=True)
    kills = db.Column(db.Integer, nullable=False)
    deaths = db.Column(db.Integer, nullable=False)
    damage = db.Column(db.Integer, nullable=False)
    hill_time = db.Column(db.Integer)
    first_bloods = db.Column(db.Integer)
    captures = db.Column(db.Integer)

    match_map = db.relationship('MatchMap', back_populates='player_data')
    player = db.relationship('Player', back_populates='player_data')