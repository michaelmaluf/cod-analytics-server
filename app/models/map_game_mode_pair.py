import uuid

from sqlalchemy.dialects.postgresql import UUID

from app import db

class MapGameModePair(db.Model):
    __tablename__ = 'map_game_mode_pairs'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    map_id = db.Column(UUID(as_uuid=True), db.ForeignKey('maps.id'), nullable=False)
    game_mode_id = db.Column(UUID(as_uuid=True), db.ForeignKey('game_modes.id'), nullable=False)

    map = db.relationship('Map', back_populates='map_game_mode_pairs')
    game_mode = db.relationship('GameMode', back_populates='map_game_mode_pairs')
    match_maps = db.relationship('MatchMap', back_populates='map_game_mode_pair')