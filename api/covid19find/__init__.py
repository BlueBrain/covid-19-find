import os

from flask import Flask, Response
from flask_cors import CORS
from .simulator import Simulator
from .simulation.getcountrydata import get_country_data


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

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
    @app.route('/api/countries/<country_code>')
    def country_details(country_code):
        (population, urban_population_percentage, urban_population_in_degraded_housing_percentage, over_65_percentage,
         hospital_employment, high_contact_population, remote_areas_population_percentage) = get_country_data(
            country_code)
        return {
            "countryCode": country_code,
            "population": population,
            "urbanPopulationPercentage": urban_population_percentage,
            "urbanPopulationInDegradedHousingPercentage": urban_population_in_degraded_housing_percentage,
            "over65Percentage": over_65_percentage,
            "hospitalEmployment": hospital_employment,
            "highContactPopulation": high_contact_population,
            "remoteAreasPopulationPercentage": remote_areas_population_percentage
        }

    @app.route("/api/simulation", methods=['POST'])
    def run_simulation():
        return Response(
            Simulator().run(),
            mimetype="text/csv"
        )

    return app
