from marshmallow import Schema, fields

class PlainUserSchema(Schema):
    id = fields.Str(required=True)
    email = fields.Str()
    username = fields.Str()
    custom = fields.Dict()

class PlainLevelSchema(Schema):
    id = fields.Str(required=True, dump_only=True)
    level_number = fields.Int()
    custom = fields.Dict()

class PlainChallengeSchema(Schema):
    id = fields.Str(required=True, dump_only=True)
    custom = fields.Dict()
    description = fields.Str()
    title = fields.Str()

class PlainActionSchema(Schema):
    id = fields.Str(required=True, dump_only=True)
    custom = fields.Dict()
    description = fields.Str()

class PlainPointSchema(Schema):
    id = fields.Str(required=True, dump_only=True)
    custom = fields.Dict()
    description = fields.Str()

class PlainPointLevelSchema(Schema):
    point = fields.Nested(PlainPointSchema())
    points_required = fields.Int()

class PlainLevelSchema(Schema):
    id = fields.Str(required=True, dump_only=True)
    level_number = fields.Int()
    custom = fields.Dict()

class UserCurrentLevelSchema(PlainLevelSchema):
    level_points_required = fields.List(fields.Nested(PlainPointLevelSchema()))

class UserChallengeSchema(Schema):
    done = fields.Boolean()
    challenge = fields.Nested(PlainChallengeSchema())

class UserPointSchema(Schema):
    points_earned = fields.Int()
    point = fields.Nested(PlainPointSchema())

class UserActionSchema(Schema):
    done_rep = fields.Int()
    action = fields.Nested(PlainActionSchema())

class LeaderboardSchema(PlainUserSchema):
    user_points = fields.List(fields.Nested(UserPointSchema()))
    user_challenges = fields.List(fields.Nested(UserChallengeSchema()))
    user_actions= fields.List(fields.Nested(UserActionSchema()))
    level = fields.Nested(PlainLevelSchema())

class LeaderboardPointSchema(Schema):
    points_earned = fields.Int()
    user = fields.Nested(PlainUserSchema())

class LeaderboardActionsSchema(Schema):
    done_rep = fields.Int()
    user = fields.Nested(PlainUserSchema())

class UserSchema(PlainUserSchema):
    pass

class UpdateUserSchema(Schema):
    email = fields.Str()
    username = fields.Str()
    custom = fields.Dict()

class DeleteUserSchema(Schema):
    message = fields.Str()
    user = fields.Nested(PlainUserSchema())

class UpdateUserActionSchema(Schema):
    value = fields.Int()