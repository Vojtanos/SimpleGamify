from db import db
from sqlalchemy.dialects.postgresql import UUID 

class PointLevelModel(db.Model):
    __tablename__ = "points_levels"

    point_id = db.Column(db.String(80), db.ForeignKey("points.id"), primary_key=True)
    level_id = db.Column(db.String(80), db.ForeignKey("levels.id"), primary_key=True)
    point = db.relationship("PointModel", back_populates="point_levels")
    level = db.relationship("LevelModel", back_populates="level_points")

    points_required = db.Column(db.Integer, default=0)