from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from flask import request, jsonify
from models import UserModel, LevelModel, ActionModel, UserActionModel, PointUserModel, PointModel, UserChallengeModel, ChallengeModel, ActionChallengeModel, PointLevelModel
from sqlalchemy.exc import SQLAlchemyError
from schemas.resources_schemas import UserSchema, UpdateUserSchema, UserChallengeSchema, UserPointSchema, UserActionSchema, UpdateUserActionSchema, DeleteUserSchema, UserCurrentLevelSchema


blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/user/<string:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    @blp.response(200, DeleteUserSchema)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting user.")
        return {"message": "User removed", "user": user}

    @blp.arguments(UpdateUserSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get_or_404(user_id)
        if "email" in user_data: user.email = user_data["email"]
        if "username" in user_data: user.username = user_data["username"]
        if "custom" in user_data: user.custom = user_data["custom"]
        db.session.add(user)
        db.session.commit()

        return user

@blp.route("/user")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        level = LevelModel.query.filter(LevelModel.level_number == 0).first()
        actions = ActionModel.query.all()
        points = PointModel.query.all()
        challenges = ChallengeModel.query.all()
        user = UserModel(**user_data, level_id = level.id)
        if UserModel.query.get(user_data["id"]):
            abort(400, message="Bad request. A user with that access point already exists.")
        try:
            # add user
            db.session.add(user)
            # add actions to user
            for action in actions:
                if not UserActionModel.query.get((user.id, action.id)):
                    user_action = UserActionModel(action_id = action.id, user_id = user.id, done_rep = 0)
                    db.session.add(user_action)
            # add challenges to user
            for challenge in challenges:
                if not UserChallengeModel.query.get((user.id, challenge.id)):
                    user_challenge = UserChallengeModel(challenge_id = challenge.id, user_id = user.id, done = False)
                    db.session.add(user_challenge)
            # add points to user
            for point in points:
                if not PointUserModel.query.get((point.id, user.id)):
                    point_user = PointUserModel(point_id = point.id, user_id = user.id, points_earned = 0)
                    db.session.add(point_user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the user.")
        return user

@blp.route("/user/<string:user_id>/challenge")
class UserChallengesDoneList(MethodView):
    @blp.response(200, UserChallengeSchema(many=True))
    def get(self, user_id):
        return UserChallengeModel.query.filter(UserChallengeModel.user_id == user_id).all()

@blp.route("/user/<string:user_id>/challenge/<string:challenge_id>")
class UserChallengeDone(MethodView):
    @blp.response(200, UserChallengeSchema)
    def get(self, user_id, challenge_id):
        return UserChallengeModel.query.get_or_404((user_id, challenge_id))

@blp.route("/user/<string:user_id>/point")
class UserPointsList(MethodView):
    @blp.response(200, UserPointSchema(many=True))
    def get(self, user_id):
        return PointUserModel.query.filter(PointUserModel.user_id == user_id).all()
    
@blp.route("/user/<string:user_id>/point/<string:point_id>")
class UserPoints(MethodView):
    @blp.response(200, UserPointSchema)
    def get(self, user_id, point_id):
        return PointUserModel.query.get_or_404((point_id, user_id))
    
@blp.route("/user/<string:user_id>/level/<string:option>")
class UserPoints(MethodView):
    @blp.response(200, UserCurrentLevelSchema)
    def get(self, user_id, option):
        user = UserModel.query.get_or_404(user_id)
        user_level = user.level
        level = user_level
        if option == "current":
            level = user_level
        if option == "next":
            level = LevelModel.query.filter(LevelModel.level_number == user_level.level_number + 1).first()
        if option == "before":
            level = LevelModel.query.filter(LevelModel.level_number == user_level.level_number - 1).first()
        if level:
            point_level = PointLevelModel.query.filter(PointLevelModel.level_id == level.id)
            level.level_points_required = point_level
        return level

@blp.route("/user/<string:user_id>/action")
class UserActionsList(MethodView):
    @blp.response(200, UserActionSchema(many=True))
    def get(self, user_id):
        return UserActionModel.query.filter(UserActionModel.user_id == user_id).all()
    
@blp.route("/user/<string:user_id>/action/<string:action_id>")
class UserAction(MethodView):
    @blp.response(200, UserActionSchema)
    def get(self, user_id, action_id):
        return UserActionModel.query.get_or_404((user_id, action_id))
    
    @blp.arguments(UpdateUserActionSchema)
    @blp.response(200, UserActionSchema)
    def put(self, data, user_id, action_id):
        # change number of times action have been done
        user_action = UserActionModel.query.get_or_404((user_id, action_id))
        user_action.done_rep = user_action.done_rep + ( data['value'] if "value" in data else 1 )
        try:
            db.session.add(user_action)
        except SQLAlchemyError:
            abort(500, message="An error occurred when doing action.")

        # if action have points attached get it to the user
        action = ActionModel.query.get(action_id)
        for action_point in action.action_points:
            if action_point.points != 0:
                point_user = PointUserModel.query.get((action_point.point.id, user_id))
                point_user.points_earned = point_user.points_earned + action_point.points
                db.session.add(point_user)

        # action may done some challenge and that may done some other challenge...
        change_occured = True
        while change_occured:
            change_occured = False
            # check all challenges that were affected by the action
            challenges = ChallengeModel.query.all()
            for challenge in challenges:
                # if user doesnt complete the challenge check if completed now
                if not UserChallengeModel.query.get((user_id, challenge.id)).done:
                    # if challenge have all sub_challenges completed
                    sub_challenges_completed = True
                    sub_challenges = challenge.challenges
                    for sub_challenge in sub_challenges:
                        if not UserChallengeModel.query.get((user_id, sub_challenge.id)).done:
                            sub_challenges_completed = False
                    # if the repetition of various actions by user is also enough to done the challenge
                    sub_actions_completed = True
                    sub_actions = challenge.challenge_actions
                    for sub_action in sub_actions:
                        if (sub_action.repetition > UserActionModel.query.get((user_id, sub_action.action.id)).done_rep):
                            sub_actions_completed = False
                    print(challenge.id, flush=True)
                    print(sub_actions_completed, flush=True)
                    print(sub_challenges_completed, flush=True)
                    # if both challenges and actions are done earn the points
                    if sub_challenges_completed and sub_actions_completed:
                        user_challenge = UserChallengeModel.query.get((user_id, challenge.id))
                        user_challenge.done = True
                        db.session.add(user_challenge)
                        # after challenge complete repeat the process if any other challenge isn't completed
                        #change_occured = True
                        # give user points for the challenge is done
                        for challenge_point in  challenge.challenge_points:
                            print(challenge_point.point.id, challenge_point.points,flush=True)
                            if challenge_point.points != 0:
                                point_user = PointUserModel.query.get((challenge_point.point.id, user_id))
                                point_user.points_earned = point_user.points_earned + challenge_point.points
                                db.session.add(point_user)
        
        # check if user reached new level (user also could reach more levels at once [while loop])
        user = UserModel.query.get(user_id)
        level_completed = True
        pluslevel = 0
        user_next_lvl = LevelModel.query.filter(LevelModel.level_number == user.level.level_number + 1).first()
        while level_completed and user_next_lvl: # user_next_lvl may not exist
            pluslevel = pluslevel + 1
            for level_point in user_next_lvl.level_points:
                user_point = PointUserModel.query.get((level_point.point.id, user_id))
                user_points_earned = user_point.points_earned
                required_points = level_point.points_required
                if user_points_earned < required_points:
                    level_completed = False
            if level_completed:
                user.level_id = user_next_lvl.id
                db.session.add(user)
                user_next_lvl = LevelModel.query.filter(LevelModel.level_number == user.level.level_number + pluslevel).first()
        db.session.commit()
        return user_action
