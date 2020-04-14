import os

from flask import Flask, Response, send_from_directory, request
from werkzeug.exceptions import BadRequestKeyError
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
import json

from .countryrepository import CountryRepository
from flask_cors import CORS
from .simulator import Simulator
from .coviddatarepository import CovidDataRepository


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    data_repo = CovidDataRepository(os.environ.get("DATA_DIR", "/tmp"))

    def update_covid_data():
        app.logger.info("Updating COVID-19 data")
        data_repo.update_data()

    update_covid_data()
    country_repo = CountryRepository()

    scheduler = BackgroundScheduler(timezone=utc)
    scheduler.add_job(func=update_covid_data, trigger="cron", hour="5")

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
                    total_pop=int(request.form["population"]),
                    hospital_beds=int(request.form["hospitalBeds"]),
                    pop_high_contact=int(request.form["highContactPopulation"]),
                    prop_urban=float(request.form["urbanPopulationProportion"]),
                    prop_isolated=float(request.form["remoteAreasPopulationProportion"]),
                    degraded=float(request.form["urbanPopulationInDegradedHousingProportion"]),
                    ge_65=float(request.form["over65Proportion"]),
                    prop_tests_hospitals=float(request.form["hospitalTestsProportion"]),
                    prop_tests_high_contact=float(request.form["highContactTestsProportion"]),
                    prop_tests_rest_of_population=float(request.form["restOfPopulationTestsProportion"]),
                    sensitivity_PCR=float(request.form["sensitivityPCR"]),
                    sensitivity_RDT=float(request.form["sensitivityRDT"]),
                    sensitivity_xray=float(request.form["sensitivityXray"]),
                    specificity_PCR=float(request.form["specificityPCR"]),
                    specificity_RDT=float(request.form["specificityRDT"]),
                    specificity_xray=float(request.form["specificityXray"]),
                    num_tests_PCR=int(request.form["numTestsPCR"]),
                    num_tests_RDT=int(request.form["numTestsRDT"]),
                    num_tests_xray=int(request.form["numTestsXray"])
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
