import uuid

from sqlalchemy.dialects.postgresql import UUID

from app import db
from app.enums import GameMode

class Map(db.Model):
    __tablename__ = 'maps'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)

    map_game_mode_pairs = db.relationship("MapGameModePair", back_populates='map')
