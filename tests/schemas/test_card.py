import pytest
from hamcrest import assert_that, has_entries
from marshmallow import ValidationError

from schemas import CardRequest


@pytest.mark.parametrize(
    "data",
    [
        ({"number": "4444555522228888", "expiration_date": "2026-02-18"}),
        ({"number": "4444555522228888", "expiration_date": "2021-02-18"}),
    ],
)
def test_valid_data(data):
    validated_data = CardRequest().load(data)
    result = CardRequest().dump(validated_data)

    assert_that(result, has_entries(data))


@pytest.mark.parametrize(
    "data, error_messages",
    [
        (
            {},
            {
                "number": ["Missing data for required field."],
                "expiration_date": ["Missing data for required field."],
            },
        ),
        (
            {"number": "1234", "expiration_date": "12"},
            {
                "number": ["Not a valid card number."],
                "expiration_date": ["Not a valid date."],
            },
        ),
    ],
)
def test_raise_validation_error(data, error_messages):
    with pytest.raises(ValidationError) as exc:
        result = CardRequest().load(data)

    assert exc.value.messages == error_messages
