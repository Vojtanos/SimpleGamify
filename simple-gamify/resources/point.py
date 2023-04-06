from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from flask import request, jsonify
from models import PointModel
from schemas.resources_schemas import PlainPointSchema


blp = Blueprint("Points", __name__, description="Operations on points")

@blp.route("/point")
class PointList(MethodView):
    @blp.response(200, PlainPointSchema(many=True))
    def get(self):
        points = PointModel.query.all()
        return points
    

@blp.route("/point/<string:point_id>")
class Point(MethodView):
    @blp.response(200, PlainPointSchema)
    def get(self, point_id):
        return PointModel.query.get_or_404(point_id)
    
    @blp.arguments(PlainPointSchema)
    @blp.response(200, PlainPointSchema)
    def put(self, point_data, point_id):
        point = PointModel.query.get_or_404(point_id)
        if "custom" in point_data: point.custom = point_data["custom"]
        if "description" in point_data: point.description = point_data["description"]
        db.session.add(point)
        db.session.commit()

        return point