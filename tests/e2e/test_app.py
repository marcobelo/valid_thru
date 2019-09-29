import requests
from hamcrest import assert_that, has_items, has_entries

BASE_URL = "http://localhost:8000"


def test_valid_thru():
    response = requests.get(f"{BASE_URL}/valid-thru/?month=02&year=2022")
    data = response.json()

    assert response.status_code == 200
    assert_that(
        data[0],
        has_items(
            "client_id", "year", "card_holder", "month", "is_active", "card_number"
        ),
    )


def test_valid_thru_bad_params():
    response = requests.get(f"{BASE_URL}/valid-thru/?month=xyz&year=abc")
    data = response.json()

    assert response.status_code == 200
    assert_that(
        data,
        has_entries(
            {"month": ["Not a valid integer."], "year": ["Not a valid integer."]}
        ),
    )
