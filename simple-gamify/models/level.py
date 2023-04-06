from db import db
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid
class LevelModel(db.Model):
    __tablename__ = "levels"

    id = db.Column(db.String(80), primary_key = True)

    level_number = db.Column(db.Integer)
    custom = db.Column(JSON)
    
    level_points = db.relationship("PointLevelModel", back_populates="level", lazy="dynamic", cascade="all, delete")
    users = db.relationship("UserModel", back_populates="level", lazy="dynamic", cascade="all, delete") # give to users variable all users with level having coresponding id