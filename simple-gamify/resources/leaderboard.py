from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from flask import request, jsonify
from models import UserModel, PointUserModel, UserActionModel, UserChallengeModel, PointModel, ActionModel
from schemas.resources_schemas import LeaderboardSchema,  LeaderboardPointSchema, LeaderboardActionsSchema


blp = Blueprint("leaderboards", __name__, description="Users stats")

@blp.route("/leaderboard")
class LeaderboardList(MethodView):
    @blp.response(200, LeaderboardSchema(many=True))
    def get(self):
        leaderboard = UserModel.query.all()
        return leaderboard

@blp.route("/leaderboard_points/<string:point_id>")
class LeaderboardByPointTypeList(MethodView):
    @blp.response(200, LeaderboardPointSchema(many=True))
    def get(self, point_id):
        PointModel.query.get_or_404(point_id)
        leaderboard = PointUserModel.query.filter(PointUserModel.point_id == point_id).order_by(PointUserModel.points_earned.desc()).all()
        return leaderboard

@blp.route("/leaderboard_actions/<string:action_id>/<string:belove_under>/<string:actions_done>")
class LeaderboardByActionsList(MethodView):
    @blp.response(200, LeaderboardActionsSchema(many=True))
    def get(self, action_id, belove_under, actions_done):
        ActionModel.query.get_or_404(action_id)
        leaderboard = None
        if belove_under == "above":
            leaderboard = UserActionModel.query.filter(UserActionModel.done_rep >= actions_done, UserActionModel.action_id == action_id).order_by(UserActionModel.done_rep.desc()).all()
        if belove_under == "below":
            leaderboard = UserActionModel.query.filter(UserActionModel.done_rep <= actions_done, UserActionModel.action_id == action_id).order_by(UserActionModel.done_rep.desc()).all()     
        return leaderboard