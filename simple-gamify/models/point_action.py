from db import db
from sqlalchemy.dialects.postgresql import UUID 

class PointActionModel(db.Model):
    __tablename__ = "points_actions"

    point_id = db.Column(db.String(80), db.ForeignKey("points.id"), primary_key=True)
    action_id = db.Column(db.String(80), db.ForeignKey("actions.id"), primary_key=True)
    point = db.relationship("PointModel", back_populates="point_actions")
    action = db.relationship("ActionModel", back_populates="action_points")

    points = db.Column(db.Integer, default=0)