import json

from flask import Flask, request
from flask_cors import CORS
from marshmallow import ValidationError

from clients import ValidThruClient
from schemas import ValidThruRequest, ValidThruResponse

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


@app.route("/client/", methods=["GET", "POST"])
def client():
    if request.method == "POST":
        client = request.json
        # TODO: Add schema to validate data
        # TODO: insert data on "database"
        # TODO: return message: (Client added.) or (Client already exist.)


if __name__ == "__main__":
    valid_thru_client = ValidThruClient()
    # valid_thru_client.populate(1000)
    valid_thru_client.populate_from_csv("app/cards.csv")

    app.run(host="0.0.0.0", port=8000)
