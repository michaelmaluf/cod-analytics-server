import uuid

from sqlalchemy.dialects.postgresql import UUID

from app import db
from app.enums import Stage


class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_one_id = db.Column(UUID(as_uuid=True), db.ForeignKey('teams.id'), nullable=False)
    team_one_maps_won = db.Column(db.Integer, nullable=False)
    team_two_id = db.Column(UUID(as_uuid=True), db.ForeignKey('teams.id'), nullable=False)
    team_two_maps_won = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    stage = db.Column(db.Enum(Stage), nullable=False)

    team_one = db.relationship('Team', back_populates='matches_as_team_one', foreign_keys=[team_one_id])
    team_two = db.relationship('Team', back_populates='matches_as_team_two', foreign_keys=[team_two_id])
    match_maps = db.relationship('MatchMap', back_populates='match')