import os

from flask import Flask, Response, send_from_directory
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

    @app.route('/api/countries')
    def countries():
        return country_repo.country_list()

    @app.route('/api/countries/<country_code>')
    def country_details(country_code):
        return country_repo.country_details(country_code)

    @app.route("/api/simulation", methods=['POST'])
    def run_simulation():
        return Response(
            Simulator().run(),
            mimetype="text/csv"
        )

    @app.route("/api/covid19data/<country_code>")
    def country_covid19_data(country_code):
        return Response(
            json.dumps(data_repo.data_for(country_code)),
            mimetype="application/json")

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
