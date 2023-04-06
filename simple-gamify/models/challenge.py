from db import db
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid
class ChallengeModel(db.Model):
    __tablename__ = "challenges"

    id = db.Column(db.String(80), primary_key = True)

    title = db.Column(db.String(80))
    description = db.Column(db.String(180))
    custom = db.Column(JSON)

    challenge_id = db.Column(db.String(80), db.ForeignKey("challenges.id"))
    challenges = db.relationship("ChallengeModel", backref=db.backref("challenge", remote_side=[id]))

    badge = db.relationship("BadgeModel", back_populates="challenge")

    challenge_actions = db.relationship("ActionChallengeModel", back_populates="challenge", lazy="dynamic", cascade="all, delete")
    challenge_users = db.relationship("UserChallengeModel", back_populates="challenge", lazy="dynamic", cascade="all, delete")
    challenge_points = db.relationship("PointChallengeModel", back_populates="challenge", lazy="dynamic", cascade="all, delete")