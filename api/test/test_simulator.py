from ..covid19find.simulator import Simulator
from ..covid19find.coviddatarepository import CovidDataRepository
import json
from jsonschema import validate
import os

path_prefix = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(path_prefix, "data")

simulator = Simulator(CovidDataRepository(data_dir))


class TestSimulator:

    def test_response_format(self):
        with open(os.path.join(path_prefix, "example-request.json")) as request_file:
            request = json.load(request_file)
        response = simulator.run(request)
        with open(os.path.join(path_prefix, "simulation-response.schema.json")) as schema_file:
            schema = json.load(schema_file)

        validate(instance=response, schema=schema)
