from db import db
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid
# this table reprezents types of points 
class PointModel(db.Model):
    __tablename__ = "points"

    id = db.Column(db.String(80), primary_key = True)
    description = db.Column(db.String(80))
    custom = db.Column(JSON)

    point_users = db.relationship("PointUserModel", back_populates="point", lazy="dynamic", cascade="all, delete")
    point_actions = db.relationship("PointActionModel", back_populates="point", lazy="dynamic", cascade="all, delete")
    point_challenges = db.relationship("PointChallengeModel", back_populates="point", lazy="dynamic", cascade="all, delete")
    point_levels = db.relationship("PointLevelModel", back_populates="point", lazy="dynamic", cascade="all, delete")
    scores = db.relationship("ScoreModel", back_populates="points", secondary="points_scores")