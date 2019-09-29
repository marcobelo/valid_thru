import pytest
from hamcrest import assert_that, has_entries
from marshmallow import ValidationError

from schemas import ValidThruRequest


def test_request_valid_data():
    data = {"month": 5, "year": 2000}
    validated_data = ValidThruRequest().load(data)

    assert_that(validated_data, has_entries(data))


@pytest.mark.parametrize(
    "data, error_messages",
    [
        (
            {},
            {
                "month": ["Missing data for required field."],
                "year": ["Missing data for required field."],
            },
        ),
        (
            {"month": "not an integer", "year": "not an integer"},
            {"month": ["Not a valid integer."], "year": ["Not a valid integer."]},
        ),
        (
            {"month": 13, "year": "2000"},
            {
                "month": [
                    "Must be greater than or equal to 1 and less than or equal to 12."
                ]
            },
        ),
    ],
)
def test_request_raise_validation_error(data, error_messages):
    with pytest.raises(ValidationError) as exc:
        result = ValidThruRequest().load(data)

    assert_that(exc.value.messages, has_entries(error_messages))
