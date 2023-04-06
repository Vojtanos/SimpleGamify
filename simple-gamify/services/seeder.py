from models import UserModel
from models import LevelModel
from models import ScoreModel
from models import DurationModel
from models import ActionModel
from models import ChallengeModel
from models import BadgeModel
from models import UserChallengeModel
from models import UserActionModel
from models import ActionChallengeModel
from models import PointModel
from models import PointActionModel
from models import PointUserModel
from models import PointScoreModel
from models import PointLevelModel
from models import PointChallengeModel
from db import db

from services.config import Config

class Seeder:
    @staticmethod
    def delete_all():
        db.session.query(UserChallengeModel).delete()
        db.session.query(UserActionModel).delete()
        db.session.query(ActionChallengeModel).delete()
        db.session.query(PointScoreModel).delete()
        db.session.query(PointLevelModel).delete()
        db.session.query(PointActionModel).delete()
        db.session.query(PointUserModel).delete()
        db.session.query(PointChallengeModel).delete()
        db.session.query(ScoreModel).delete()
        db.session.query(PointModel).delete()
        db.session.query(UserModel).delete()
        db.session.query(ActionModel).delete()
        db.session.query(ChallengeModel).delete()
        db.session.query(BadgeModel).delete()
        db.session.query(DurationModel).delete()
        db.session.query(LevelModel).delete()
        db.session.commit()
    
    @staticmethod
    def add_config(config_path):
        config = Config(config_path)
        required = False
        config.validate(required)
        Seeder.__insert_config_to_db(config)

    @staticmethod
    def insert_config():
        config_path = 'gamification-config'
        config = Config(config_path)
        config.validate()
        Seeder.__insert_config_to_db(config)
    
    @staticmethod
    def connect_users_to_new_config():
        actions = ActionModel.query.all()
        points = PointModel.query.all()
        challenges = ChallengeModel.query.all()
        users = UserModel.query.all()
        for user in users:
            # add new actions to users
            for action in actions:
                if not UserActionModel.query.get((user.id, action.id)):
                    user_action = UserActionModel(action_id = action.id, user_id = user.id, done_rep = 0)
                    db.session.add(user_action)
            # add new challenges to users
            for challenge in challenges:
                if not UserChallengeModel.query.get((user.id, challenge.id)):
                    user_challenge = UserChallengeModel(challenge_id = challenge.id, user_id = user.id, done = False)
                    db.session.add(user_challenge)
            # add new points_types to users
            for point in points:
                if not PointUserModel.query.get((point.id, user.id)):
                    point_user = PointUserModel(point_id = point.id, user_id = user.id, points_earned = 0)
                    db.session.add(point_user)

    @classmethod
    def __insert_config_to_db(cls, config):
        # insert points
        for point_system_id in config.points_systems.keys():
            custom = config.points_systems[point_system_id]["custom"] if "custom" in config.points_systems[point_system_id] else ""
            description = config.points_systems[point_system_id]["desc"] if "desc" in config.points_systems[point_system_id] else ""
            point = PointModel(id=point_system_id, custom = custom, description = description)
            db.session.add(point)

        # insert levels
        i = LevelModel.query.count()
        for level_id in config.levels.keys():
            level = i
            i = i + 1
            custom = config.levels[level_id]["custom"] if "custom" in config.levels[level_id] else ""
            level = LevelModel(level_number = level, id=level_id, custom = custom)
            db.session.add(level)

            points_types = config.levels[level_id]["points"] if "points" in config.levels[level_id] else ""

            if points_types != "":
                for point_id in points_types.keys():
                    points_required = points_types[point_id]
                    point_level = PointLevelModel(point_id = point_id,level_id = level_id, points_required = points_required)
                    db.session.add(point_level)

        # insert actions
        for action_id in config.actions.keys():
            custom = config.actions[action_id]["custom"] if "custom" in config.actions[action_id] else ""
            description = config.actions[action_id]["desc"] if "desc" in config.actions[action_id] else ""
            action = ActionModel(id=action_id, custom = custom, description = description)
            db.session.add(action)

            points_types = config.actions[action_id]["points"] if "points" in config.actions[action_id] else ""

            if points_types != "":
                for point_id in points_types.keys():
                    points = points_types[point_id]
                    point_action = PointActionModel(point_id = point_id, action_id = action_id, points = points)
                    db.session.add(point_action)
        
        # insert challenges
        for challenge_id in config.challenges.keys():
            custom = config.challenges[challenge_id]["custom"] if "custom" in config.challenges[challenge_id] else ""
            description = config.challenges[challenge_id]["desc"] if "desc" in config.challenges[challenge_id] else ""
            title = config.challenges[challenge_id]["title"] if "title" in config.challenges[challenge_id] else ""
            action = ChallengeModel(id=challenge_id, custom = custom, description = description, title = title)
            db.session.add(action)

            points_types = config.challenges[challenge_id]["points"] if "points" in config.challenges[challenge_id] else ""
            if points_types != "":
                for point_id in points_types.keys():
                    points = points_types[point_id]
                    point_challenge = PointChallengeModel(point_id = point_id, challenge_id = challenge_id, points = points)
                    db.session.add(point_challenge)

            challenges = config.challenges[challenge_id]["challenges"] if "challenges" in config.challenges[challenge_id] else ""
            if challenges != "":
                for challenge_required_id in challenges:
                    challenge = ChallengeModel.query.get(challenge_required_id)
                    if challenge:
                        challenge.challenge_id = challenge_id
            
            actions = config.challenges[challenge_id]["actions"] if "actions" in config.challenges[challenge_id] else ""
            if actions != "":
                for action_id in actions.keys():
                    repetition = actions[action_id]
                    action_challenge = ActionChallengeModel(repetition = repetition, challenge_id = challenge_id, action_id = action_id)
                    db.session.add(action_challenge)

            # badge = config.challenges[challenge_id]["badge"] if "badge" in config.challenges[challenge_id] else ""
            # if badge != "":
            #     custom = badge["custom"] if "custom" in badge else ""
            #     description = badge["desc"] if "desc" in badge else ""
            #     title = badge["title"] if "title" in badge else ""
            #     badge = BadgeModel(challenge_id=challenge_id, custom = custom, description = description, title = title)
            #     db.session.add(badge)
            #     db.session.commit()

        print("New schema inserted!")