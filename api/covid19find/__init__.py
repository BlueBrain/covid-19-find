import os

from flask import Flask, Response, send_from_directory, request, make_response, jsonify
from flask_expects_json import expects_json
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
import json

from .countryrepository import CountryRepository
from flask_cors import CORS
from .simulator import Simulator
from .coviddatarepository import CovidDataRepository
from .simulation.covidlib import cl_path_prefix


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    data_repo = CovidDataRepository(os.environ.get("DATA_DIR", "/tmp"))

    def update_covid_data():
        app.logger.info("Updating COVID-19 data.")
        data_repo.update_data()
        app.logger.info("Finished updating COVID-19 data.")

    country_repo = CountryRepository()

    scheduler = BackgroundScheduler(timezone=utc)
    scheduler.add_job(func=update_covid_data, trigger='interval', hours=2)
    scheduler.add_job(func=update_covid_data)
    scheduler.start()

    def not_found_if_none(data, country_code):
        if data is None:
            return Response(response=json.dumps({
                "status": 404,
                "error": "Couldn't find data for country " + country_code
            }), status=404, mimetype="application/json")
        else:
            return jsonify(data)

    app_path_prefix = os.getenv("PUBLIC_URL", "")

    @app.route(f'{app_path_prefix}/api/countries')
    def countries():
        return jsonify(country_repo.country_list())

    @app.route(f'{app_path_prefix}/api/countries/<country_code>')
    def country_details(country_code):
        return not_found_if_none(country_repo.country_details(country_code), country_code)

    with open(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), "simulation-request.schema.json")) as schema_file:
        schema = json.load(schema_file)

    @app.route(f'{app_path_prefix}/api/scenarios')
    def fetch_scenarios():
        return simulator.default_scenarios()

    @app.route(f'{app_path_prefix}/api/covid19data/<country_code>')
    def country_covid19_data(country_code):
        return not_found_if_none(data_repo.data_for(country_code), country_code)

    parameters_dir = os.path.join(cl_path_prefix, os.environ.get("PARAMETERS_DIRECTORY", "BBP_testing"))
    simulator = Simulator(data_repo, parameters_dir)

    @app.route(f'{app_path_prefix}/api/simulation', methods=['POST'])
    @expects_json(schema)
    def run_simulation():
        request_data = request.get_json()
        return jsonify(simulator.run(request_data))

    static_files_dir = os.path.abspath(os.environ.get("STATIC_DATA_DIR"))

    @app.route(f'{app_path_prefix}/')
    def index():
        response = make_response(send_from_directory(static_files_dir,
                                                     'index.html', as_attachment=False))
        response.headers["Cache-Control"] = "no-cache, must-revalidate"
        return response

    @app.route(f'{app_path_prefix}/<path:filename>')
    def static_files(filename):
        return send_from_directory(static_files_dir,
                                   filename, as_attachment=False)

    return app
