import uuid

from sqlalchemy.dialects.postgresql import UUID

from app import db
from app.enums import GameModeType

class GameMode(db.Model):
    __tablename__ = 'game_modes'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Enum(GameModeType), nullable=False)

    map_game_mode_pairs = db.relationship("MapGameModePair", back_populates='game_mode')