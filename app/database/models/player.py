import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import db

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    hardpoint_rank = db.Column(db.Integer)
    search_and_destroy_rank = db.Column(db.Integer)
    control_rank = db.Column(db.Integer)

    team_statuses = relationship("PlayerTeamStatus", back_populates="player")
    player_data = db.relationship('PlayerData', back_populates='player', lazy='dynamic')
