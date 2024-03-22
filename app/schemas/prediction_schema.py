from marshmallow import Schema, fields


class PredictionRequestSchema(Schema):
    team_one_name = fields.String()
    team_two_name = fields.String()
    game_mode = fields.String()
    map = fields.String()


class PlayerAveragesSchema(Schema):
    kills = fields.Integer()
    deaths = fields.Integer()
    damage = fields.Integer()
    objectives = fields.Integer()


class PredictionResponseSchema(Schema):
    team_one_prediction = fields.Integer()
    team_two_prediction = fields.Integer()
    team_one_player_predictions = fields.Dict(keys=fields.Str(), values=fields.Nested(PlayerAveragesSchema()))
    team_two_player_predictions = fields.Dict(keys=fields.Str(), values=fields.Nested(PlayerAveragesSchema()))
    team_one_average_score = fields.Float()
    team_two_average_score = fields.Float()
    team_one_average_score_against = fields.Float()
    team_two_average_score_against = fields.Float()
    team_one_average_kd = fields.Float()
    team_two_average_kd = fields.Float()
    league_average_score = fields.Float()
    league_average_kd = fields.Float()


