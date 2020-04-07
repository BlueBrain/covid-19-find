import os

from flask import Flask, Response
from .simulator import Simulator


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple hardcoded list of countries
    @app.route('/api/countries')
    def countries():
        return {
            "countries": [{
                "countryCode": "CH",
                "name": "Switzerland"
            }]
        }

    # a simple hardcoded list of countries
    @app.route('/api/countries/CH')
    def country_details():
        return {
            "countryCode": "CH",
            "name": "Switzerland",
            "population": 8570000
        }

    @app.route("/api/simulation", methods=['POST'])
    def run_simulation():
        return Response(
            Simulator().run(),
            mimetype="text/csv"
        )

    return app
