import json
import csv
import math
import os
from datetime import date, timedelta, datetime

import pandas as pd

from .simulation.covidlib import run_simulation, get_system_params, cl_path_prefix

import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/simulation")

import cdata

INCOME_CATEGORY_LABEL_TO_CODE = {
    "Low income": "L",
    "Lower middle income": "LM",
    "Upper middle income": "UM",
    "High income": "H",
    None: None
}
INCOME_CATEGORY_CODE_TO_LABEL = dict([(v, k) for (k, v) in INCOME_CATEGORY_LABEL_TO_CODE.items()])


class Simulator:

    def __init__(self, covid_repository, parameters_directory="production"):
        self.covid_repository = covid_repository
        self.parameters_directory = parameters_directory
        self.past_phases = self.__load_past_phases()

    @staticmethod
    def __map_datapoint(dp):
        return {
            "Date": dp["date"],
            "accumulated_deaths": dp["totalDeaths"],
            "accumulated_cases": dp["totalConfirmed"],
            "tests": 0 if dp["newTests"] is None else dp["newTests"]
        }

    def get_country_df(self, country_code):
        covid_data = self.covid_repository.data_for(country_code)["timeseries"]
        return pd.DataFrame.from_records(list(map(self.__map_datapoint, covid_data)))

    def get_fixed_parameters(self, parameters):
        return {
            "total_pop": parameters["population"],
            "prop_15_64": parameters["activePopulationProportion"],
            "age_gt_64": parameters["over64Proportion"],
            "prop_urban": parameters["urbanPopulationProportion"],
            "staff_per_bed": parameters["hospitalStaffPerBed"],
            "fatality_reduction": parameters["fatalityReduction"],
            "income_category": INCOME_CATEGORY_LABEL_TO_CODE[parameters["incomeCategory"]],
            "test_directory": self.parameters_directory
        }

    @staticmethod
    def get_scenario_parameters(parameters):
        return list(map(Simulator.__map_scenario, parameters["scenarios"]))

    @staticmethod
    def __map_scenario(input_scenario):
        phases = input_scenario["phases"]
        return {
            "imported_infections_per_day": Simulator.__get_array_for_key(phases, "importedInfectionsPerDay"),
            "severity": Simulator.__get_array_for_key(phases, "severity"),
            "trig_values": Simulator.__get_array_for_key(phases, "trigger"),
            "trig_def_type": Simulator.__get_array_for_key(phases, "triggerType"),
            "trig_op_type": Simulator.__get_array_for_key(phases, "triggerCondition"),
            "prop_contacts_traced": Simulator.__get_array_for_key(phases, "proportionOfContactsTraced"),
            "num_tests_mitigation": Simulator.__get_array_for_key(phases, "numTestsMitigation"),
            "type_tests_mitigation": Simulator.__get_array_for_key(phases, "typeTestsMitigation"),
            "test_strategy": Simulator.__get_array_for_key(phases, "testingStrategy"),
            "sensitivity": Simulator.__get_array_for_key(phases, "sensitivity"),
            "specificity": Simulator.__get_array_for_key(phases, "specificity"),
            "test_multipliers": [0, 1, 2, 3],
            "num_tests_care": Simulator.__get_array_for_key(phases, "numTestsCare"),
            "type_tests_care": Simulator.__get_array_for_key(phases, "typeTestsCare"),
            "requireddxtests": Simulator.__get_array_for_key(phases, "requiredDxTests"),
            "results_period": Simulator.__get_array_for_key(phases, "resultsPeriod"),
            "fatality_reduction_recent": Simulator.__get_array_for_key(phases, "fatalityReductionRecent")
        }

    @staticmethod
    def __get_array_for_key(scenarios, key, func=lambda x: x):
        return list(map(lambda scenario: func(scenario[key]), scenarios))

    @staticmethod
    def __tests_dataframe_row_to_response(index_row):
        row = index_row[1]
        return {
            "tests": None if math.isnan(row["tests administered"]) else int(row["tests administered"]),
            "livesSaved": None if math.isnan(row["lives saved"]) else row["lives saved"]
        }

    @staticmethod
    def __tests_dataframe_to_response(test_df):
        return list(map(Simulator.__tests_dataframe_row_to_response, test_df.iterrows()))

    def run(self, parameters):
        country_code = parameters["countryCode"]
        scenarios = self.get_scenario_parameters(parameters)
        country_df = self.get_country_df(country_code)

        fixed_parameters = self.get_fixed_parameters(parameters)
        fixed_parameters["expert_mode"] = False
        fixed_parameters["past_severities"] = self.__past_phases_for(country_code)["severities"]
        fixed_parameters["past_dates"] = self.__past_phases_for(country_code)["dates"]
        fixed_parameters["run_multiple_test_scenarios"] = True

        overrideableFixedParams = get_system_params(self.parameters_directory)
        overrideableFixedParams.update(cdata.getcountryparams(country_code))

        overrideableFixedParams.update(fixed_parameters)

        result = run_simulation(country_df, overrideableFixedParams, scenarios=scenarios)

        scenario_data = []
        scenario_dfs = result[0]
        scenario_totals = result[2]
        test_df = result[1]
        for i in range(0, len(scenario_totals["total_deaths_by_scenario"])):
            scenarios_compartments_df = scenario_dfs[i * 2]
            scenario_data.append(
                {
                    "totalTests": int(scenario_totals["total_tests_mit_by_scenario"][i]),
                    "totalDeaths": int(scenario_totals["total_deaths_by_scenario"][i]),
                    "totalPositiveTests": int(scenario_totals["total_cases_by_scenario"][i]),
                    "maxInfected": int(scenario_totals["max_infected_by_scenario"][i]),
                    "totalInfected": int(scenario_totals["total_infected_by_scenario"][i]),
                    "maxIsolated": int(scenario_totals["max_isolated_by_scenario"][i]),
                    "testsNeededForCare": int(scenario_totals["total_tests_care_by_scenario"][i]),
                    "testsNeededForMitigation": int(scenario_totals["total_tests_mit_by_scenario"][i]),
                    "data": {
                        "hospitals": self.__dataframe_to_response(
                            scenarios_compartments_df[scenarios_compartments_df.compartment.eq("Hospitals")]),
                        "otherHighContact": self.__dataframe_to_response(
                            scenarios_compartments_df[scenarios_compartments_df.compartment.eq("Other high contact ")]),
                        "restOfPopulation": self.__dataframe_to_response(
                            scenarios_compartments_df[scenarios_compartments_df.compartment.eq("Rest of population")]),
                        "total": self.__total_dataframe_to_response(scenario_dfs[i * 2 + 1])
                    },
                    "testingImpact": self.__tests_dataframe_to_response(test_df[test_df.scenario.eq(i)]),
                    "samplesRequiredForSerologicalStudies": self.__get_serological_data(i, scenario_totals)
                }
            )
        return {"scenarios": scenario_data, "score": self.__past_phases_for(country_code)["score"]}

    @staticmethod
    def __get_serological_data(scenario_index, scenario_totals):
        result = []
        for i in [5, 10, 100, 1000]:
            result.append(
                {
                    "numSubgroups": i,
                    "testsRequired": int(scenario_totals["total_serotests_by_scenario_{}".format(i)][scenario_index])
                }
            )

        return result

    @staticmethod
    def __dataframe_to_response(df):
        return list(map(Simulator.__dataframe_row_to_response, df.iterrows()))

    @staticmethod
    def __total_dataframe_to_response(df):
        return list(map(Simulator.__total_dataframe_row_to_response, df.iterrows()))

    @staticmethod
    def __total_dataframe_row_to_response(index_row):
        row = index_row[1]
        result = Simulator.__dataframe_row_to_response(index_row)
        result["actualDeaths"] = None if math.isnan(row["actualnewdeaths"]) else int(row["actualnewdeaths"])
        result["actualCases"] = None if math.isnan(row["actualnewcases"]) else int(row["actualnewcases"])
        result["actualTests"] = None if math.isnan(row["actualnewtests_mit"]) else int(row["actualnewtests_mit"])
        return result

    @staticmethod
    def __dataframe_row_to_response(index_row):
        row = index_row[1]
        rEff = row.get("reff", math.nan)
        return {
            "day": int(row["days"]),
            "date": row["dates"].date().isoformat(),
            "population": int(row["population"]),
            "susceptibles": int(row["susceptibles"]),
            "currentIsolated": int(row["isolated"]),
            "currentInfected": int(row["infected"]),
            "totalConfirmed": int(row["confirmed"]),
            "totalInfected": int(row["accumulatedinfected"]),
            "totalTested": int(row["tested_mit"]),
            "currentInfectedNotIsolated": int(row["infectednotisolated"]),
            "totalDeaths": int(row["deaths"]),
            "totalRecovered": int(row["recovered"]),
            "beta": row["beta"],
            "rEff": None if math.isnan(rEff) else rEff,
            "susceptibleProportion": row["susceptibleprop"],
            "newTests": int(row["newtested_mit"]),
            "newInfected": int(row["newinfected"]),
            "newConfirmed": int(row["newconfirmed"]),
            "newIsolated": int(row["newisolated"]),
            "newIsolatedInfected": int(row["newisolatedinfected"]),
            "newRecovered": int(row["newrecovered"]),
            "requiredDxTests": int(row["requireddxtests"]),
            "actualDxTest": int(row["actualdxtests"]),
            "newDeaths": int(row["newdeaths"]),
            "truePositives": int(row["truepositives"]),
            "falsePositives": int(row["falsepositives"]),
            "trueNegatives": int(row["truenegatives"]),
            "falseNegatives": int(row["falsenegatives"]),
            "ppv": None if math.isnan(row["ppv"]) else row["ppv"],
            "npv": None if math.isnan(row["npv"]) else row["npv"],
            "incidence": row["incidence"],
            "prevalence": row["prevalence"],
            "newTestsPositiveProportion": row.get("positive_rate", None),
            "detectionRate": row.get("detection_rate", None)
        }

    def __reverse_map_scenario(self, covid_libscenario):
        phases = []
        phase1 = {
            "importedInfectionsPerDay": covid_libscenario["imported_infections_per_day"],
            "trigger": date.today().isoformat(),
            "triggerType": covid_libscenario["trig_def_type"],
            "triggerCondition": covid_libscenario["trig_op_type"],
            "severity": covid_libscenario["severity"],
            "proportionOfContactsTraced": covid_libscenario["prop_contacts_traced"],
            "numTestsMitigation": int(covid_libscenario["num_tests_mitigation"]),
            "typeTestsMitigation": "PCR",
            "specificity": float(covid_libscenario["specificity"]),
            "sensitivity": float(covid_libscenario["sensitivity"]),
            "testingStrategy": covid_libscenario["test_strategy"],
            "numTestsCare": int(covid_libscenario["num_tests_care"]),
            "typeTestsCare": "PCR",
            "requiredDxTests": int(covid_libscenario["requireddxtests"]),
            "resultsPeriod": int(covid_libscenario["results_period"]),
            "fatalityReductionRecent": covid_libscenario["fatality_reduction_recent"]
        }
        phase2 = dict(phase1)
        phase2["trigger"] = (date.today() + timedelta(days=10)).isoformat()
        # we only have one phase but frontend requires two
        phases.append(phase1)
        phases.append(phase2)

        return {"phases": phases}

    def __load_past_phases(self):
        past_phases = {}
        with open(os.path.join(cl_path_prefix, "db1.csv")) as past_phases_file:
            csv_reader = csv.reader(past_phases_file, delimiter=',')
            # skip header
            next(csv_reader)
            for row in csv_reader:
                country_code = row[1]
                past_phases[country_code] = {
                    "severities": json.loads(row[3]),
                    "dates": json.loads(row[4]),
                    "score": float(row[5])
                }

        return past_phases

    def default_scenarios(self):
        with open(os.path.join(cl_path_prefix, self.parameters_directory, "default_parameters.json")) as params_file:
            scenarios_from_file = json.load(params_file)
        scenarios = list(map(self.__reverse_map_scenario, scenarios_from_file))
        with open(os.path.join(cl_path_prefix, self.parameters_directory, "system_params.json")) as params_file:
            fixed_parameters_from_file = json.load(params_file)
        return {
            "scenarios": scenarios,
            "fatalityReduction": fixed_parameters_from_file["fatality_reduction"]
        }

    def __past_phases_for(self, country_code):
        return self.past_phases.get(country_code, {
            "severities": [],
            "dates": [],
            "score": None
        })
