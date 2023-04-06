from db import db
from sqlalchemy.dialects.postgresql import UUID 

class PointChallengeModel(db.Model):
    __tablename__ = "points_challenges"

    point_id = db.Column(db.String(80), db.ForeignKey("points.id"), primary_key=True)
    challenge_id = db.Column(db.String(80), db.ForeignKey("challenges.id"), primary_key=True)
    point = db.relationship("PointModel", back_populates="point_challenges")
    challenge = db.relationship("ChallengeModel", back_populates="challenge_points")

    points = db.Column(db.Integer, default=0)