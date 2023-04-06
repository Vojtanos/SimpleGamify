from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from flask import request, jsonify
from models import ChallengeModel
from schemas.resources_schemas import PlainChallengeSchema


blp = Blueprint("challenges", __name__, description="Operations on challenges")

@blp.route("/challenge")
class ChallengeList(MethodView):
    @blp.response(200, PlainChallengeSchema(many=True))
    def get(self):
        challenges = ChallengeModel.query.all()
        return challenges
    

@blp.route("/challenge/<string:challenge_id>")
class Challenge(MethodView):
    @blp.response(200, PlainChallengeSchema)
    def get(self, challenge_id):
        return ChallengeModel.query.get_or_404(challenge_id)
    
    @blp.arguments(PlainChallengeSchema)
    @blp.response(200, PlainChallengeSchema)
    def put(self, challenge_data, challenge_id):
        challenge = ChallengeModel.query.get_or_404(challenge_id)
        if "title" in challenge_data: challenge.title = challenge_data["title"]
        if "description" in challenge_data: challenge.description = challenge_data["description"]
        if "custom" in challenge_data: challenge.custom = challenge_data["custom"]
        db.session.add(challenge)
        db.session.commit()

        return challenge