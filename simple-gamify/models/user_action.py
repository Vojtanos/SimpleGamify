from db import db
from sqlalchemy.dialects.postgresql import UUID 

class UserActionModel(db.Model):
    __tablename__ = "users_actions"

    user_id = db.Column(db.String(80), db.ForeignKey("users.id"), primary_key=True)
    action_id = db.Column(db.String(80), db.ForeignKey("actions.id"), primary_key=True)
    action = db.relationship("ActionModel", back_populates="action_users")
    user = db.relationship("UserModel", back_populates="user_actions")

    done_rep = db.Column(db.Integer)