from clients import ValidThruClient


def test_populate_in_memory():
    valid_thru_client = ValidThruClient()
    valid_thru_client.populate(100)

    assert len(valid_thru_client._clients) == 100
    assert valid_thru_client._client_id_counter == 101
    assert len(valid_thru_client._cards) == 100
