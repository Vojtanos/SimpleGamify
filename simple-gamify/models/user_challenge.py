from db import db
from sqlalchemy.dialects.postgresql import UUID 
import uuid

class UserChallengeModel(db.Model):
    __tablename__ = "users_challenges"

    user_id = db.Column(db.String(80), db.ForeignKey("users.id"), primary_key=True)
    challenge_id = db.Column(db.String(80), db.ForeignKey("challenges.id"), primary_key=True)
    challenge = db.relationship("ChallengeModel", back_populates="challenge_users")
    user = db.relationship("UserModel", back_populates="user_challenges")

    done = db.Column(db.Boolean)