from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from flask import request, jsonify
from models import LevelModel
from schemas.resources_schemas import PlainLevelSchema


blp = Blueprint("Levels", __name__, description="Operations on levels")

@blp.route("/level")
class LevelList(MethodView):
    @blp.response(200, PlainLevelSchema(many=True))
    def get(self):
        levels = LevelModel.query.all()
        return levels
    

@blp.route("/level/<string:level_id>")
class Level(MethodView):
    @blp.response(200, PlainLevelSchema)
    def get(self, level_id):
        return LevelModel.query.get_or_404(level_id)
    
    @blp.arguments(PlainLevelSchema)
    @blp.response(200, PlainLevelSchema)
    def put(self, level_data, level_id):
        level = LevelModel.query.get_or_404(level_id)
        if "custom" in level_data: level.custom = level_data["custom"]
        db.session.add(level)
        db.session.commit()

        return level