import os
from flask import Flask
from flask_smorest import Api
from debugger import debugger
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from services.custom_cli import blp as CustomCliBlueprint

from db import db

import models

from resources.user import blp as UserBlueprint
from resources.leaderboard import blp as LeaderboardBlueprint
from resources.challenge import blp as ChallengeBlueprint
from resources.action import blp as ActionBlueprint
from resources.level import blp as LevelBlueprint
from resources.point import blp as PointBlueprint

def create_app():
   debugger() # init debugger if DEBBUGER=True
   app = Flask(__name__) # init Flask 
   # configurate swagger and db
   app.config["API_TITLE"] = "SIMPLE-GAMIFY REST API"
   app.config["API_VERSION"] = "v1"
   app.config["OPENAPI_VERSION"] = "3.0.3"
   app.config["OPENAPI_URL_PREFIX"] = "/"
   app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
   app.config[
      "OPENAPI_SWAGGER_UI_URL"
   ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
   app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
   app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
   app.config["PROPAGATE_EXCEPTIONS"] = True

   db.init_app(app) # register db to app
   api = Api(app) # create flask-smorest for open API

   engine = create_engine(os.environ.get('DATABASE_URL'))
   # create database in posgre if not exists
   if not database_exists(engine.url): # Checks for the first time  
      create_database(engine.url)     # Create new DB    
      print("New database created.") # Verifies if database is there or not.
   
   # create all tables defined with models
   with app.app_context():
      db.create_all()

   # register endpoints
   api.register_blueprint(UserBlueprint)
   api.register_blueprint(LeaderboardBlueprint)
   api.register_blueprint(ChallengeBlueprint)
   api.register_blueprint(ActionBlueprint)
   api.register_blueprint(LevelBlueprint)
   api.register_blueprint(PointBlueprint)

   # register custom-cli commands
   app.register_blueprint(CustomCliBlueprint)

   return app