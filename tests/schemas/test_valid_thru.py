import pytest
from hamcrest import assert_that, has_entries
from marshmallow import ValidationError

from schemas import ValidThruRequest, ValidThruResponse


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


def test_response_valid_data():
    data = {
        "client_id": 1,
        "card_holder": "John Do",
        "card_number": "1111444422223333",
        "month": 5,
        "year": 2000,
        "is_active": False,
    }
    validated_data = ValidThruResponse().load(data)

    assert_that(validated_data, has_entries(data))


@pytest.mark.parametrize(
    "data, error_messages",
    [
        (
            {},
            {
                "client_id": ["Missing data for required field."],
                "card_holder": ["Missing data for required field."],
                "card_number": ["Missing data for required field."],
                "month": ["Missing data for required field."],
                "year": ["Missing data for required field."],
                "is_active": ["Missing data for required field."],
            },
        ),
        (
            {
                "client_id": "asd",
                "card_holder": 123,
                "card_number": 123,
                "month": "asd",
                "year": "asd",
                "is_active": "asd",
            },
            {
                "card_holder": ["Not a valid string."],
                "card_number": ["Not a valid string."],
                "client_id": ["Not a valid integer."],
                "is_active": ["Not a valid boolean."],
                "month": ["Not a valid integer."],
                "year": ["Not a valid integer."],
            },
        ),
        (
            {
                "client_id": 1,
                "card_holder": "John Do",
                "card_number": "1111444422223333",
                "month": 13,
                "year": 2000,
                "is_active": False,
            },
            {
                "month": [
                    "Must be greater than or equal to 1 and less than or equal to 12."
                ]
            },
        ),
    ],
)
def test_response_raise_validation_error(data, error_messages):
    with pytest.raises(ValidationError) as exc:
        result = ValidThruResponse().load(data)

    assert exc.value.messages == error_messages
