import csv
import random
from datetime import date

from faker import Faker

fake = Faker()


# client_id, number, expiration_date, name, address, dob

with open("cards.csv", "a", newline="") as file:
    wrt = csv.writer(file, delimiter="|")
    id_counter = 1
    for i in range(10000):
        client = {
            "name": fake.name(),
            "dob": fake.date_of_birth().isoformat(),
            "address": fake.address().split("\n")[0],
        }
        n_cards = random.randint(1, 5)

        for n_card in range(n_cards):
            month, year = fake.credit_card_expire().split("/")
            card = {
                "number": fake.credit_card_number(card_type="mastercard"),
                "expiration_date": date(
                    int(f"20{year}"), int(f"{month}"), 1
                ).isoformat(),
            }
            wrt.writerow(
                [
                    id_counter,
                    card["number"],
                    card["expiration_date"],
                    client["name"],
                    client["address"],
                    client["dob"],
                ]
            )
        id_counter += 1
