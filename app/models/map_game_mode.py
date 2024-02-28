import uuid

from sqlalchemy.dialects.postgresql import UUID

from app import db
from app.enums import GameModeType

class MapGameModePair(db.Model):
    __tablename__ = 'map_game_mode_pairs'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    map_id = db.Column(UUID(as_uuid=True), db.ForeignKey('maps.id'), nullable=False)
    game_mode_id = db.Column(UUID(as_uuid=True), db.ForeignKey('game_modes.id'), nullable=False)

    map = db.relationship('Map', back_populates='map_game_mode_pairs')
    game_mode = db.relationship('GameMode', back_populates='map_game_mode_pairs')
    match_maps = db.relationship('MatchMap', back_populates='map_game_mode_pair')

class Map(db.Model):
    __tablename__ = 'maps'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)

    map_game_mode_pairs = db.relationship('MapGameModePair', back_populates='map')


class GameMode(db.Model):
    __tablename__ = 'game_modes'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Enum(GameModeType), nullable=False)

    map_game_mode_pairs = db.relationship("MapGameModePair", back_populates='game_mode')