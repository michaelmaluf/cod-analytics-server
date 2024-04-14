from sqlalchemy.dialects.postgresql import UUID

from app.database import db

class PlayerTeamStatus(db.Model):
    __tablename__ = 'player_team_status'
    player_id = db.Column(UUID(as_uuid=True), db.ForeignKey('players.id'), primary_key=True)
    team_id = db.Column(UUID(as_uuid=True), db.ForeignKey('teams.id'), primary_key=True)
    active = db.Column(db.Boolean, default=True)

    player = db.relationship('Player', back_populates='team_statuses', lazy='joined')
    team = db.relationship('Team', back_populates='player_statuses')