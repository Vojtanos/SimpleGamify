from db import db
from sqlalchemy.dialects.postgresql import UUID 

class PointUserModel(db.Model):
    __tablename__ = "points_users"

    point_id = db.Column(db.String(80), db.ForeignKey("points.id"), primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey("users.id"), primary_key=True)
    point = db.relationship("PointModel", back_populates="point_users")
    user = db.relationship("UserModel", back_populates="user_points")
    
    points_earned = db.Column(db.Integer, default=0)