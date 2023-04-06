from db import db
from sqlalchemy.dialects.postgresql import UUID 
import uuid
class ScoreModel(db.Model):
    __tablename__ = "scores"

    id = db.Column(db.String(80), primary_key = True)

    last_to = db.Column(db.DateTime(timezone=False), nullable=False)
    challenges_done = db.Column(db.Integer, nullable=False)
    points_done = db.Column(db.Integer, nullable=False)

    points = db.relationship("PointModel", back_populates="scores", secondary="points_scores")
    
    duration_id = db.Column(db.String(80), db.ForeignKey("durations.id"))
    duration = db.relationship("DurationModel", back_populates="scores")
    user_id = db.Column(db.String(80), db.ForeignKey("users.id"))
    user = db.relationship("UserModel", back_populates="scores")


