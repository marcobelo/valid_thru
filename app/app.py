import json

from flask import Flask, request
from flask_cors import CORS

from clients import ValidThruClient
from schemas import ValidThruRequest, ValidThruResponse

app = Flask(__name__)
CORS(app)


@app.route("/valid-thru/")  # ?month=02&year=2020
def valid_thru():
    data = {"month": request.args.get("month"), "year": request.args.get("year")}
    validated_data = ValidThruRequest().load(data)
    response_data = valid_thru_client.cards_valid_thru_this_month_year(validated_data)
    validated_response = ValidThruResponse(many=True).load(response_data)

    return json.dumps(validated_response)


if __name__ == "__main__":
    valid_thru_client = ValidThruClient()
    valid_thru_client.populate(1000)

    app.run(host="0.0.0.0", port=8000)
