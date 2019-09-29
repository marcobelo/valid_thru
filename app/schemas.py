from marshmallow import Schema, EXCLUDE, pre_load
from marshmallow.fields import Integer
from marshmallow.validate import Range


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
