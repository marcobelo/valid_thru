import json

from flask import Flask, request
from flask_cors import CORS
from schemas import ValidThruRequest

app = Flask(__name__)
CORS(app)


@app.route("/valid-thru/")  # ?month=02&year=2020
def valid_thru():
    data = {"month": request.args.get("month"), "year": request.args.get("year")}
    validated_data = ValidThruRequest().load(data)
    # TODO: Create Client to get data
    # TODO: Create validation for response
    return json.dumps(validated_data)


if __name__ == "__main__":
    # TODO: Populate data (in memory) from here
    app.run(host="0.0.0.0", port=8000)
