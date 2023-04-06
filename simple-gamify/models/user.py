from db import db
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(80), primary_key=True)

    username = db.Column(db.String(80), default="")
    email = db.Column(db.String(80), default="")
    custom = db.Column(JSON)

    level_id = db.Column(db.String(80), db.ForeignKey("levels.id"), nullable=False) # db.ForeingKey restrict that id have already exists
    level = db.relationship("LevelModel", back_populates="users")   # relationship - automaticly populate level = levelmodel with coresponding id 
                                                                    # backpopulates - give reference to LevelModel reprezentet as list of users
    scores = db.relationship("ScoreModel", back_populates="user", lazy="dynamic")
                                                                    
    user_challenges = db.relationship("UserChallengeModel", back_populates="user", lazy="dynamic", cascade="all, delete")
    user_actions = db.relationship("UserActionModel", back_populates="user", lazy="dynamic", cascade="all, delete")
    user_points = db.relationship("PointUserModel", back_populates="user", lazy="dynamic", cascade="all, delete")