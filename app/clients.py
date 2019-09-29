from datetime import date

from faker import Faker


class ValidThruClient:
    def __init__(self):
        self._cards = []
        self._clients = []
        self._client_id_counter = 1

    def populate(self, amount):
        fake = Faker()
        for i in range(amount):
            client = {
                "id": self._client_id_counter,
                "name": fake.name(),
                "dob": fake.date_of_birth(),
                "address": fake.address().split("\n")[0],
            }
            month, year = fake.credit_card_expire().split("/")
            card = {
                "number": fake.credit_card_number(card_type="mastercard"),
                "expiration_date": date(
                    int(f"20{year}"), int(f"{month}"), 1
                ).isoformat(),
            }
            self._clients.append(client)
            self._cards.append(card)
            self._client_id_counter += 1
