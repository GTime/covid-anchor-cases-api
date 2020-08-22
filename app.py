from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

# Constants
# COVID_CASES_API = {
#     "all": "https://coronavirus-19-api.herokuapp.com/all",
#     "country": "https://coronavirus-19-api.herokuapp.com/countries",
# }
COVID_CASES_API = "https://coronavirus-19-api.herokuapp.com/countries"


# Creating flask app
app = Flask(__name__)
cors = CORS(app)


# Helper
def get_country(data_list, country):
    for item in data_list:
        if item.country is country:
            return item

# Filter


class Filter():
    data_list = []
    result = []
    query = {
        "skip": None,
        "take": None
    }

    def __init__(self, data_list, query):
        self.result = data_list
        self.query = {**self.query, **query}

    def filter(self):
        # Doing Skip
        skip = self.query["skip"]
        if skip is not None:
            self.result = self.result[skip:]

        # Doing Take
        take = self.query["take"]
        if (take is not None) and (len(self.result) > take):
            self.result = self.result[0:take]

        return self.result


# TESTING THE CODE "ONE-TWO"
# cases = [
#     "World",
#     "USA",
#     "Brazil",
#     "India",
#     "Russia",
#     "South Africa"
# ]

# cases_filter = Filter(cases, {"skip": 3, "take": 2})
# filtered = cases_filter.filter()

# print(len(filtered))
# print(filtered)


# Routes
@app.route("/")
def home():
    query = {}

    # Check for take
    if "take" in request.args:
        query.update({"take": int(request.args["take"])})

    # Check for skip
    if "skip" in request.args:
        query.update({"skip": int(request.args["skip"])})

    # Make a request to get our cases data
    response = requests.get(COVID_CASES_API)
    data = list(response.json())

    # Filter Data
    data_filter = Filter(data, query)
    data = data_filter.filter()

    # print(type(data_filter.result))
    return jsonify(data_filter.result)
