import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.database import db

class MLModel(db.Model):
    __tablename__ = 'ml_models'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_mode_id = db.Column(UUID(as_uuid=True), db.ForeignKey('game_modes.id'), nullable=False)
    hyperparameters = db.Column(JSONB, nullable=False)
    model_data = db.Column(db.LargeBinary, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.now)
    updated_date = db.Column(db.DateTime, default=datetime.now)

    game_mode = db.relationship("GameMode", back_populates='ml_models')