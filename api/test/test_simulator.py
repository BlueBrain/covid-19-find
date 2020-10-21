from ..covid19find.simulator import Simulator
from ..covid19find.coviddatarepository import CovidDataRepository
import json
from jsonschema import validate
import os
import pytest

path_prefix = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(path_prefix, "data")
simulation_test_data_dir = os.path.join(path_prefix, "../covid19find/simulation")

simulator = Simulator(CovidDataRepository(data_dir),
                      parameters_directory=os.path.join(simulation_test_data_dir, "test1"))


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

    @pytest.mark.parametrize("test_folder",
                             ["test1", "test1_1", "test1_2", "test1_3", "test1_4", "test1_5", "test1_6", "test1_7",
                              "test1_8"])
    def test_scenario_results(self, test_folder):
        params_dir = os.path.join(simulation_test_data_dir, test_folder)
        simulator.parameters_directory = params_dir
        with open(os.path.join(params_dir, "parameters.json")) as params_file:
            params = json.load(params_file)
        req = {"countryCode": "CH",
               "population": params["fixed_params"]["total_pop"],
               "activePopulationProportion": params["fixed_params"]["prop_15_64"],
               "hospitalBeds": params["fixed_params"]["hospital_beds"],
               "hospitalStaffPerBed": params["fixed_params"]["staff_per_bed"],
               "workingOutsideHomeProportion": params["fixed_params"]["prop_woh"],
               "urbanPopulationProportion": params["fixed_params"]["prop_urban"],
               "over64Proportion": params["fixed_params"]["age_gt_64"],
               "belowPovertyLineProportion": params["fixed_params"]["prop_below_pl"],
               "scenarios": list(map(map_scenario, params["scenario_params"]))}
        response = simulator.run(req)
        with open(os.path.join(params_dir, "result_summary.csv")) as res_summary_file:
            res_summary = res_summary_file.read()
        expected_result = int(float(res_summary.split(",")[1].strip()))
        assert response["scenarios"][0]["totalDeaths"] == expected_result


def map_scenario(scenario_from_params):
    scenario = {}
    phases = []
    for i in range(0, len(scenario_from_params["symptomatic_only"])):
        phases.append({
            "importedInfectionsPerDay": scenario_from_params["imported_infections_per_day"][i],
            "trigger": scenario_from_params["trig_values"][i],
            "triggerType": scenario_from_params["trig_def_type"][i],
            "triggerCondition": scenario_from_params["trig_op_type"][i],
            "severity": scenario_from_params["severity"][i],
            "proportionOfContactsTraced": scenario_from_params["prop_contacts_traced"][i],
            "numTestsMitigation": scenario_from_params["num_tests_mitigation"][i],
            "typeTestsMitigation": scenario_from_params["type_test_mitigation"][i],
            "specificity": scenario_from_params["specificity"][i],
            "sensitivity": scenario_from_params["sensitivity"][i],
            "testSymptomaticOnly": scenario_from_params["symptomatic_only"][i],
            
            "numTestsCare": scenario_from_params["num_tests_care"][i],
            "typeTestsCare": scenario_from_params["type_tests_care"][i],
            "requiredDxTests": scenario_from_params["requireddxtests"][i],
        })

    scenario["phases"] = phases
    return scenario
