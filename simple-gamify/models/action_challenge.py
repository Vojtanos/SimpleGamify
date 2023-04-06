from db import db
from sqlalchemy.dialects.postgresql import UUID 

class ActionChallengeModel(db.Model):
    __tablename__ = "actions_challenges"

    action_id = db.Column(db.String(80), db.ForeignKey("actions.id"), primary_key=True)
    challenge_id = db.Column(db.String(80), db.ForeignKey("challenges.id"), primary_key=True)
    action = db.relationship("ActionModel", back_populates="action_challenges")
    challenge = db.relationship("ChallengeModel", back_populates="challenge_actions")
    repetition = db.Column(db.Integer, default=1)