import marshmallow as ma


class PredictionRequestSchema(ma.Schema):
    team_one_name = ma.fields.String()
    team_two_name = ma.fields.String()
    game_mode = ma.fields.String()
    map = ma.fields.String()


class PredictionResponseSchema(ma.Schema):
    team_one_score = ma.fields.Integer()
    team_two_score = ma.fields.Integer()
