from db import db
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid

class BadgeModel(db.Model):
    __tablename__ = "badges"

    id = db.Column(db.String(80), primary_key = True)
    challenge_id = db.Column(db.String(80), db.ForeignKey('challenges.id'))
    challenge = db.relationship("ChallengeModel", back_populates="badge")

    title = db.Column(db.String(80))
    description = db.Column(db.String(180))
    custom = db.Column(JSON)