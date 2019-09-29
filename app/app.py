import json

from flask import Flask, request
from flask_cors import CORS
from marshmallow import ValidationError

from clients import ValidThruClient
from schemas import CardRequest, ClientRequest, ValidThruRequest, ValidThruResponse

app = Flask(__name__)
CORS(app)


@app.route("/valid-thru/", methods=["GET"])  # ?month=02&year=2020
def valid_thru():
    data = {"month": request.args.get("month"), "year": request.args.get("year")}

    try:
        validated_data = ValidThruRequest().load(data)
        response_data = valid_thru_client.cards_valid_thru_this_month_year(
            validated_data
        )
        validated_response = ValidThruResponse(many=True).load(response_data)
    except ValidationError as exc:
        return json.dumps(exc.messages)

    return json.dumps(validated_response)


@app.route("/client/", methods=["GET", "POST", "PUT", "DELETE"])
def client():
    if request.method == "POST":
        client = request.json
        client = ClientRequest().load(client)
        result = valid_thru_client.add_client(client)

        return json.dumps(result)

    elif request.method == "GET":  # ?id=3
        client_id = int(request.args.get("id"))
        result = valid_thru_client.get_client(client_id)

        return json.dumps(result)

    elif request.method == "PUT":  # ?id=3
        client_id = int(request.args.get("id"))
        client = request.json
        client = ClientRequest().load(client)
        result = valid_thru_client.update_client(client_id, client)

        return json.dumps(result)

    elif request.method == "DELETE":  # ?id=3
        client_id = int(request.args.get("id"))
        result = valid_thru_client.delete_client(client_id)

        return json.dumps(result)


@app.route("/card/", methods=["POST"])
def card():
    if request.method == "POST":  # ?client_id=3
        client_id = int(request.args.get("client_id"))
        card = request.json
        card = CardRequest().load(card)
        result = valid_thru_client.add_card(client_id, card)

        return json.dumps(result)


if __name__ == "__main__":
    valid_thru_client = ValidThruClient()
    # valid_thru_client.populate(1000)
    valid_thru_client.populate_from_csv("app/cards.csv")

    app.run(host="0.0.0.0", port=8000)
