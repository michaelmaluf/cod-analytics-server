from marshmallow import Schema, fields, ValidationError

class EnumField(fields.Field):
    def __init__(self, enum, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum = enum

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return self.enum(value)
        except ValueError:
            raise ValidationError(f"'{value}' is not a valid {self.enum.__name__}")