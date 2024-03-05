import uuid

from sqlalchemy.dialects.postgresql import UUID

from database import db

class MatchMap(db.Model):
    __tablename__ = 'match_maps'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id = db.Column(UUID(as_uuid=True), db.ForeignKey('matches.id'), nullable=False)
    map_game_mode_id = db.Column(UUID(as_uuid=True), db.ForeignKey('map_game_mode_pairs.id'), nullable=False)
    map_number = db.Column(db.Integer, nullable=False)
    team_one_score = db.Column(db.Integer, nullable=False)
    team_two_score = db.Column(db.Integer, nullable=False)

    match = db.relationship('Match', back_populates='match_maps')
    map_game_mode_pair = db.relationship('MapGameModePair', back_populates='match_maps')
    player_data = db.relationship('PlayerData', back_populates='match_map')