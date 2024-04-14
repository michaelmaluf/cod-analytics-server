from marshmallow import Schema, fields


class PlayersByTeamRequestSchema(Schema):
    team_name = fields.String()


class PlayersByTeamResponseSchema(Schema):
    players = fields.List(fields.String())
