import uuid

from sqlalchemy.dialects.postgresql import UUID

from app import db
from app.enums import GameMode

class Map(db.Model):
    __tablename__ = 'maps'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    game_mode = db.Column(db.Enum(GameMode), nullable=False)

    match_maps = db.relationship("MatchMap", back_populates='map')