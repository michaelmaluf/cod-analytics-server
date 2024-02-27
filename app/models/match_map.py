import uuid

from sqlalchemy.dialects.postgresql import UUID

from app import db

class MatchMap(db.Model):
    __tablename__ = 'match_maps'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id = db.Column(UUID(as_uuid=True), db.ForeignKey('matches.id'))
    map_id = db.Column(UUID(as_uuid=True), db.ForeignKey('maps.id'))
    map_number = db.Column(db.Integer, nullable=False)
    team_one_score = db.Column(db.Integer, nullable=False)
    team_two_score = db.Column(db.Integer, nullable=False)

    match = db.relationship('Match', back_populates='match_maps')
    map = db.relationship('Map', back_populates='match_maps')
    player_data = db.relationship('PlayerData', back_populates='match_map')