from marshmallow import Schema, fields, EXCLUDE
from app.enums import Stage
from .enum_schema import EnumField

class MatchSchema(Schema):
    id = fields.UUID(dump_only=True)
    team_one_maps_won = fields.Integer(required=True)
    team_two_maps_won = fields.Integer(required=True)
    date = fields.DateTime(format='%m/%d/%Y, %I:%M:%S %p',  required=True)
    stage = EnumField(Stage, required=True)
    lan = fields.Boolean(required=True)

    class Meta:
        unknown = EXCLUDE

