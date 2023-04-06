from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from flask import request, jsonify
from models import ActionModel
from schemas.resources_schemas import PlainActionSchema


blp = Blueprint("Actions", __name__, description="Operations on actions")

@blp.route("/action")
class ActionList(MethodView):
    @blp.response(200, PlainActionSchema(many=True))
    def get(self):
        actions = ActionModel.query.all()
        return actions
    

@blp.route("/action/<string:action_id>")
class Action(MethodView):
    @blp.response(200, PlainActionSchema)
    def get(self, action_id):
        return ActionModel.query.get_or_404(action_id)
    
    @blp.arguments(PlainActionSchema)
    @blp.response(200, PlainActionSchema)
    def put(self, action_data, action_id):
        action = ActionModel.query.get_or_404(action_id)
        if "description" in action_data: action.description = action_data["description"]
        if "custom" in action_data: action.custom = action_data["custom"]
        db.session.add(action)
        db.session.commit()

        return action