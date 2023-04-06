from db import db
from sqlalchemy.dialects.postgresql import UUID 

class PointScoreModel(db.Model):
    __tablename__ = "points_scores"

    point_id = db.Column(db.String(80), db.ForeignKey("points.id"), primary_key=True)
    score_id = db.Column(db.String(80), db.ForeignKey("scores.id"), primary_key=True)
    
    points_earned = db.Column(db.Integer, default=0)