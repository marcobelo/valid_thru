import pytest
from hamcrest import assert_that, has_entries
from marshmallow import ValidationError

from schemas import ClientRequest


def test_valid_data():
    data = {
        "name": "Marco Barone Belo",
        "dob": "1990-06-04",
        "address": "Arnaldo St, 123",
    }
    validated_data = ClientRequest().load(data)
    result = ClientRequest().dump(validated_data)

    assert_that(result, has_entries(data))


@pytest.mark.parametrize(
    "data, error_messages",
    [
        (
            {},
            {
                "address": ["Missing data for required field."],
                "dob": ["Missing data for required field."],
                "name": ["Missing data for required field."],
            },
        ),
        (
            {"name": "   ", "dob": "   ", "address": "   "},
            {
                "address": ["Field cannot be empty."],
                "dob": ["Not a valid date."],
                "name": ["Field cannot be empty."],
            },
        ),
        (
            {"name": 123, "dob": "not a dob", "address": 123},
            {
                "address": ["Not a valid string."],
                "dob": ["Not a valid date."],
                "name": ["Not a valid string."],
            },
        ),
    ],
)
def test_raise_validation_error(data, error_messages):
    with pytest.raises(ValidationError) as exc:
        result = ClientRequest().load(data)

    assert exc.value.messages == error_messages
