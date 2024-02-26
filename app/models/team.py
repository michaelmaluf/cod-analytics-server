import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app import db

class Team(db.Model):
    __tablename__ = 'teams'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(db.String(100), nullable=False)
    players = relationship('Player', secondary='player_team_status', back_populates='teams')