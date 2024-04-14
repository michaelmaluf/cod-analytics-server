import uuid

from sqlalchemy.dialects.postgresql import UUID

from app.database import db

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)

    player_statuses = db.relationship("PlayerTeamStatus", back_populates="team", lazy='joined')
    matches_as_team_one = db.relationship('Match',
                                          foreign_keys='[Match.team_one_id]',
                                          back_populates='team_one',
                                          lazy='dynamic')
    matches_as_team_two = db.relationship('Match',
                                          foreign_keys='[Match.team_two_id]',
                                          back_populates='team_two',
                                          lazy='dynamic')