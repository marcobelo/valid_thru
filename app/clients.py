import csv
from datetime import date
from schemas import ClientRequest

from faker import Faker


class ValidThruClient:
    def __init__(self):
        self._cards = []
        self._clients = {}
        self._client_id_counter = 1

    def populate_from_csv(self, filepath):
        with open(filepath, newline="") as file:
            reader = csv.reader(file, delimiter="|")
            for line in reader:
                card = {
                    "client_id": int(line[0]),
                    "number": line[1],
                    "expiration_date": date(*[int(ymd) for ymd in line[2].split("-")]),
                }
                client = {
                    "name": line[3],
                    "address": line[4],
                    "dob": date(*[int(ymd) for ymd in line[5].split("-")]),
                }
                self._cards.append(card)
                try:
                    self._clients[int(line[0])]
                except KeyError:
                    self._clients[int(line[0])] = client
                    self._client_id_counter = int(line[0]) + 1

    def populate(self, amount):
        fake = Faker()
        for i in range(amount):
            client = {
                "name": fake.name(),
                "dob": fake.date_of_birth(),
                "address": fake.address().split("\n")[0],
            }
            month, year = fake.credit_card_expire().split("/")
            card = {
                "client_id": self._client_id_counter,
                "number": fake.credit_card_number(card_type="mastercard"),
                "expiration_date": date(int(f"20{year}"), int(f"{month}"), 1),
            }
            self._clients[self._client_id_counter] = client
            self._cards.append(card)
            self._client_id_counter += 1

    def cards_valid_thru_this_month_year(self, data):
        today = date.today()
        is_active = True
        if (data["year"] < today.year) or (
            data["year"] == today.year and data["month"] < today.month
        ):
            is_active = False

        near_to_expire = []
        for card in self._cards:
            if card["expiration_date"].year == data["year"]:
                if card["expiration_date"].month == data["month"]:
                    client = self._clients[card["client_id"]]
                    near_to_expire.append(
                        {
                            "client_id": card["client_id"],
                            "card_holder": client["name"],
                            "card_number": card["number"],
                            "month": data["month"],
                            "year": data["year"],
                            "is_active": is_active,
                        }
                    )
        return near_to_expire

    def add_client(self, data):
        for client_id, client in self._clients.items():
            if data["name"] == client["name"]:
                if (
                    data["address"] == client["address"]
                    and data["dob"] == client["dob"]
                ):
                    return {
                        "message": "Client already on our database.",
                        "client_id": client_id,
                    }

        self._clients[self._client_id_counter] = data
        self._client_id_counter += 1

        return {
            "message": "Client added with success.",
            "client_id": self._client_id_counter - 1,
        }

    def get_client(self, client_id):
        try:
            return ClientRequest().dump(self._clients[client_id])
        except KeyError:
            return {"message": "Client not found."}

    def update_client(self, client_id, data):
        id_found = False
        try:
            for _client_id, _client in self._clients.items():
                if client_id == _client_id:
                    id_found = True
                if data["name"] == _client["name"]:
                    if (
                        data["address"] == _client["address"]
                        and data["dob"] == _client["dob"]
                    ):
                        return {
                            "message": "Cannot update, this client is already registered.",
                            "client_id": _client_id,
                        }
            if id_found:
                self._clients[client_id] = data
                return {
                    "message": "Client updated with success.",
                    "client_id": client_id,
                }
            return {"message": "Client id not found.", "client_id": client_id}

        except KeyError:
            return {"message": "Client doesn't exists."}

    def delete_client(self, client_id):
        try:
            del self._clients[client_id]
            return {"message": "Client delete with success."}
        except KeyError:
            return {"message": "Client not found.", "client_id": client_id}

