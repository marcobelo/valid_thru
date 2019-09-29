from hamcrest import assert_that, has_entries
from datetime import date
from clients import ValidThruClient
from schemas import ClientRequest


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


def test_cards_valid_thru_testing_is_active_equal_False():
    valid_thru_client = ValidThruClient()
    valid_thru_client.populate(1)
    client = valid_thru_client._clients[1]
    valid_thru_client._cards[0]["expiration_date"] = date(2019, 5, 1)
    period = {"month": 5, "year": 2019}
    cards = valid_thru_client.cards_valid_thru_this_month_year(period)

    assert cards[0]["is_active"] == False


def test_add_client_and_add_existing_client():
    data = {"name": "Marco B", "address": "Some st", "dob": "1990-06-04"}
    client = ClientRequest().load(data)
    valid_thru_client = ValidThruClient()
    result = valid_thru_client.add_client(client)
    assert_that(
        result, has_entries({"message": "Client added with success.", "client_id": 1})
    )

    # Adding an existing client
    result = valid_thru_client.add_client(client)
    assert_that(
        result,
        has_entries({"message": "Client already on our database.", "client_id": 1}),
    )


def test_get_client_valid_id_and_invalid_id():
    data = {"name": "Marco B", "address": "Some st", "dob": "1990-06-04"}
    client = ClientRequest().load(data)
    valid_thru_client = ValidThruClient()
    add_client = valid_thru_client.add_client(client)
    result = valid_thru_client.get_client(1)

    assert_that(result, has_entries(data))

    result = valid_thru_client.get_client(2)

    assert_that(result, has_entries({"message": "Client not found."}))


def test_update_client_success_and_try_to_overwrite():
    data = {"name": "Marco B", "address": "Some st", "dob": "1990-06-04"}
    to_update = {"name": "Marco Barone", "address": "Some street", "dob": "1990-06-01"}
    client = ClientRequest().load(data)
    valid_thru_client = ValidThruClient()
    add_client = valid_thru_client.add_client(client)

    result = valid_thru_client.update_client(1, to_update)

    assert_that(
        result, has_entries({"message": "Client updated with success.", "client_id": 1})
    )
    result = valid_thru_client.update_client(1, to_update)

    assert_that(
        result,
        has_entries(
            {
                "message": "Cannot update, this client is already registered.",
                "client_id": 1,
            }
        ),
    )


def test_update_client_doesnt_exist():
    to_update = {"name": "Marco Barone", "address": "Some street", "dob": "1990-06-01"}
    valid_thru_client = ValidThruClient()
    result = valid_thru_client.update_client(1, to_update)

    assert_that(result, has_entries({"message": "Client doesn't exists."}))


def test_delete_client():
    client = {"name": "Marco Barone", "address": "Some street", "dob": "1990-06-01"}
    card_1 = {"number": "1111555522228888", "expiration_date": "2026-02-01"}
    card_2 = {"number": "2222555522228888", "expiration_date": "2019-12-15"}
    valid_thru_client = ValidThruClient()
    result = valid_thru_client.add_client(client)
    result = valid_thru_client.add_card(1, card_1)
    result = valid_thru_client.add_card(1, card_2)

    result = valid_thru_client.delete_client(1)

    assert_that(result, has_entries({"message": "Client delete with success."}))

    assert len(valid_thru_client._cards) == 0
    assert len(valid_thru_client._clients) == 0


def test_delete_client_not_found():
    valid_thru_client = ValidThruClient()
    result = valid_thru_client.delete_client(1)

    assert_that(result, has_entries({"message": "Client not found.", "client_id": 1}))


def test_add_card_client_not_found():
    card = {"number": "1111555522228888", "expiration_date": "2026-02-01"}
    valid_thru_client = ValidThruClient()
    result = valid_thru_client.add_card(1, card)

    assert_that(result, has_entries({"message": "Client not found.", "client_id": 1}))
