from marshmallow import EXCLUDE, Schema, pre_load
from marshmallow.fields import Boolean, Integer, String
from marshmallow.validate import Length, Range


class BaseSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    @pre_load
    def strip_strings_fields(self, data, **kwargs):
        for key, value in data.items():
            if type(value) is str:
                data[key] = data[key].strip()

        return data


class ValidThruRequest(BaseSchema):
    month = Integer(required=True, validate=Range(min=1, max=12))
    year = Integer(required=True)


class ValidThruResponse(BaseSchema):
    client_id = Integer(required=True)
    card_holder = String(required=True)
    card_number = String(
        required=True, validate=Length(equal=16, error="Not a valid card number.")
    )
    month = Integer(required=True, validate=Range(min=1, max=12))
    year = Integer(required=True)
    is_active = Boolean(required=True)
