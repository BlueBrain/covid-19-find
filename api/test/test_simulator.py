from ..covid19find.simulator import Simulator
from ..covid19find.coviddatarepository import CovidDataRepository
import json
from jsonschema import validate
import os

path_prefix = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(path_prefix, "data")
simulation_test_data_dir = os.path.join(path_prefix, "../covid19find/simulation")

simulator = Simulator(CovidDataRepository(data_dir),
                      parameters_directory=os.path.join(simulation_test_data_dir, "BBP_testing"))


class TestSimulator:

    def test_response_format(self):
        default_scenarios = simulator.default_scenarios()
        request = {
            "countryCode": "CH",
            "population": 8655000,
            "activePopulationProportion": 0.66,
            "hospitalBeds": 34620,
            "hospitalStaffPerBed": 2.5,
            "workingOutsideHomeProportion": 0.2,
            "urbanPopulationProportion": 0.73,
            "over64Proportion": 0.20,
            "belowPovertyLineProportion": 0.10,
            "scenarios": default_scenarios
        }
        response = simulator.run(request)
        with open(os.path.join(path_prefix, "simulation-response.schema.json")) as schema_file:
            schema = json.load(schema_file)

        validate(instance=response, schema=schema)

    def test_default_scenarios(self):
        with open(os.path.join(path_prefix, "../covid19find/simulation-request.schema.json")) as schema_file:
            schema = json.load(schema_file)

        default_scenarios = simulator.default_scenarios()
        request = {
            "countryCode": "CH",
            "population": 8655000,
            "activePopulationProportion": 0.66,
            "hospitalBeds": 34620,
            "hospitalStaffPerBed": 2.5,
            "workingOutsideHomeProportion": 0.2,
            "urbanPopulationProportion": 0.73,
            "over64Proportion": 0.20,
            "belowPovertyLineProportion": 0.10,
            "scenarios": default_scenarios
        }
        validate(instance=request, schema=schema)