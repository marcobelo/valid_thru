from datetime import date
from clients import ValidThruClient


def test_populate_in_memory():
    valid_thru_client = ValidThruClient()
    valid_thru_client.populate(100)

    assert len(valid_thru_client._clients) == 100
    assert valid_thru_client._client_id_counter == 101
    assert len(valid_thru_client._cards) == 100


def test_populate_from_csv_in_memory():
    valid_thru_client = ValidThruClient()
    valid_thru_client.populate_from_csv("app/cards.csv")

    assert len(valid_thru_client._clients) == 10000
    assert valid_thru_client._client_id_counter == 10001
    assert len(valid_thru_client._cards) == 30068


def test_get_cards_valid_thru_that_month_and_year():
    valid_thru_client = ValidThruClient()
    valid_thru_client.populate(1000)
    period = {"month": 2, "year": 2028}

    cards_to_expire = valid_thru_client.cards_valid_thru_this_month_year(period)

    _cards_to_expire = [
        card
        for card in valid_thru_client._cards
        if card["expiration_date"].year == period["year"]
        and card["expiration_date"].month == period["month"]
    ]

    assert len(cards_to_expire) == len(_cards_to_expire)


def test_cards_valid_thru_testing_is_active_boolean():
    valid_thru_client = ValidThruClient()
    valid_thru_client.populate(1)
    client = valid_thru_client._clients[1]
    valid_thru_client._cards[0]["expiration_date"] = date(2019, 5, 1)
    period = {"month": 5, "year": 2019}
    cards = valid_thru_client.cards_valid_thru_this_month_year(period)

    assert cards[0]["is_active"] == False
