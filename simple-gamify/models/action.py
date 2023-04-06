from db import db
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid
class ActionModel(db.Model):
    __tablename__ = "actions"

    id = db.Column(db.String(80), primary_key = True)

    description = db.Column(db.String(180))
    custom = db.Column(JSON)

    action_challenges = db.relationship("ActionChallengeModel", back_populates="action", lazy="dynamic", cascade="all, delete")
    action_points = db.relationship("PointActionModel", back_populates="action", lazy="dynamic", cascade="all, delete")
    action_users = db.relationship("UserActionModel", back_populates="action", lazy="dynamic", cascade="all, delete")