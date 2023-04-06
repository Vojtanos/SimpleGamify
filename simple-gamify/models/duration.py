from db import db
from sqlalchemy.dialects.postgresql import UUID 
import uuid

class DurationModel(db.Model):
    __tablename__ = "durations"

    id = db.Column(db.String(80), primary_key = True)

    duration = db.Column(db.Integer, nullable=False)
    last_to = db.Column(db.DateTime(timezone=False))

    scores = db.relationship("ScoreModel", back_populates="duration", lazy="dynamic", cascade="all, delete")