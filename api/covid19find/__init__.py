import os

from flask import Flask, Response, send_from_directory, request
from werkzeug.exceptions import BadRequestKeyError
import json

from .countryrepository import CountryRepository
from flask_cors import CORS
from .simulator import Simulator
from .coviddatarepository import CovidDataRepository


def create_app():
    # create and configure the app

    data_repo = CovidDataRepository(os.environ.get("DATA_DIR", "/tmp"))
    data_repo.update_data()
    country_repo = CountryRepository()
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    def not_found_if_none(data, country_code):
        if data is None:
            return Response(response=json.dumps({
                "status": 404,
                "error": "Couldn't find data for country " + country_code
            }), status=404, mimetype="application/json")
        else:
            return data

    @app.route('/api/countries')
    def countries():
        return country_repo.country_list()

    @app.route('/api/countries/<country_code>')
    def country_details(country_code):
        return not_found_if_none(country_repo.country_details(country_code), country_code)

    @app.route("/api/simulation", methods=['POST'])
    def run_simulation():
        try:
            return {
                "scenarios": Simulator().run(
                    total_pop=request.form["total_pop"],
                    pop_hospitals=request.form["pop_hospitals"],
                    pop_high_contact=request.form["pop_high_contact"],
                    prop_urban=request.form["prop_urban"],
                    prop_isolated=request.form["prop_isolated"],
                    degraded=request.form["degraded"],
                    ge_65=request.form["ge_65"],
                    prop_tests_hospitals=request.form["prop_tests_hospitals"],
                    prop_tests_high_contact=request.form["prop_tests_high_contact"],
                    prop_tests_rest_of_population=request.form["prop_tests_rest_of_population"],
                    sensitivity_PCR=request.form["sensitivity_PCR"],
                    sensitivity_RDT=request.form["sensitivity_RDT"],
                    sensitivity_xray=request.form["sensitivity_xray"],
                    selectivity_PCR=request.form["selectivity_PCR"],
                    selectivity_RDT=request.form["selectivity_RDT"],
                    selectivity_xray=request.form["selectivity_xray"],
                    num_tests_PCR=request.form["num_tests_PCR"],
                    num_tests_RDT=request.form["num_tests_RDT"],
                    num_tests_xray=request.form["num_tests_xray"]
                )
            }
        except BadRequestKeyError as bke:
            return Response(
                json.dumps({
                    "status": 400,
                    "error": "Missing form parameter: '" + bke.args[0] + "'."
                }),
                status=400
            )

    @app.route("/api/covid19data/<country_code>")
    def country_covid19_data(country_code):
        return not_found_if_none(data_repo.data_for(country_code), country_code)

    static_files_dir = os.path.abspath(os.environ.get("STATIC_DATA_DIR"))

    @app.route('/')
    def index():
        return send_from_directory(static_files_dir,
                                   'index.html', as_attachment=False)

    @app.route('/<path:filename>')
    def static_files(filename):
        return send_from_directory(static_files_dir,
                                   filename, as_attachment=False)

    return app
