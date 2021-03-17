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
        request = simulator.default_scenarios()
        request["countryCode"] = "CH"
        request["population"] = 8655000
        request["activePopulationProportion"] = 0.66
        request["hospitalBeds"] = 34620
        request["hospitalStaffPerBed"] = 2.5
        request["workingOutsideHomeProportion"] = 0.2
        request["urbanPopulationProportion"] = 0.73
        request["over64Proportion"] = 0.20
        request["belowPovertyLineProportion"] = 0.10
        request["incomeCategory"] = "High income"

        response = simulator.run(request)
        with open(os.path.join(path_prefix, "simulation-response.schema.json")) as schema_file:
            schema = json.load(schema_file)

        validate(instance=response, schema=schema)

    def test_default_scenarios(self):
        with open(os.path.join(path_prefix, "../covid19find/simulation-request.schema.json")) as schema_file:
            schema = json.load(schema_file)

        request = simulator.default_scenarios()
        request["countryCode"] = "CH"
        request["population"] = 8655000
        request["activePopulationProportion"] = 0.66
        request["hospitalBeds"] = 34620
        request["hospitalStaffPerBed"] = 2.5
        request["workingOutsideHomeProportion"] = 0.2
        request["urbanPopulationProportion"] = 0.73
        request["over64Proportion"] = 0.20
        request["belowPovertyLineProportion"] = 0.10
        request["incomeCategory"] = "High income"

        validate(instance=request, schema=schema)
