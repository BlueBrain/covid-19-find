import json
import math
import os
from datetime import date

import pandas as pd

from .simulation.covidlib import run_simulation, get_system_params, cl_path_prefix


class Simulator:
    IS_SCENARIO_COUNTERFACTUAL = [False, False, False]

    def __init__(self, covid_repository, parameters_directory="production"):
        self.covid_repository = covid_repository
        self.parameters_directory = parameters_directory

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
            "hospital_beds": parameters["hospitalBeds"],
            "prop_15_64": parameters["activePopulationProportion"],
            "age_gt_64": parameters["over64Proportion"],
            "prop_urban": parameters["urbanPopulationProportion"],
            "prop_below_pl": parameters["belowPovertyLineProportion"],
            "prop_woh": parameters["workingOutsideHomeProportion"],
            "staff_per_bed": parameters["hospitalStaffPerBed"],
            "test_directory": self.parameters_directory
        }

    @staticmethod
    def get_scenario_parameters(parameters):
        return [Simulator.__map_scenario(i, scenario) for i, scenario in enumerate(parameters["scenarios"])]

    @staticmethod
    def __map_scenario(index, input_scenario):
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
            "is_counterfactual": [str(Simulator.IS_SCENARIO_COUNTERFACTUAL[index]) for _ in range(len(phases))]
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
        scenarios = self.get_scenario_parameters(parameters)
        country_df = self.get_country_df(parameters["countryCode"])
        fixed_parameters = self.get_fixed_parameters(parameters)
        fixed_parameters["expert_mode"] = False
        # TODO remove after tests
        with open(os.path.join(self.parameters_directory, "parameters.json")) as params_file:
            params_from_file = json.load(params_file)

        fixed_parameters["past_severities"] = params_from_file["fixed_params"]["past_severities"]
        fixed_parameters["past_dates"] = params_from_file["fixed_params"]["past_dates"]
        fixed_parameters["expert_mode"] = params_from_file["fixed_params"]["expert_mode"]

        result = run_simulation(country_df, fixed_parameters, scenarios=scenarios)

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
                    "maxInfected": int(scenario_totals["max_infected_by_scenario"][i]),
                    "totalInfected": int(scenario_totals["total_infected_by_scenario"][i]),
                    "maxIsolated": int(scenario_totals["max_isolated_by_scenario"][i]),
                    "data": {
                        "hospitals": self.__dataframe_to_response(
                            scenarios_compartments_df[scenarios_compartments_df.compartment.eq("Hospitals")]),
                        "otherHighContact": self.__dataframe_to_response(
                            scenarios_compartments_df[scenarios_compartments_df.compartment.eq("Other high contact ")]),
                        "restOfPopulation": self.__dataframe_to_response(
                            scenarios_compartments_df[scenarios_compartments_df.compartment.eq("Rest of population")]),
                        "total": self.__dataframe_to_response(scenario_dfs[i * 2 + 1])
                    },
                    "testingImpact": self.__tests_dataframe_to_response(test_df[test_df.scenario.eq(i)])
                }
            )
        return {"scenarios": scenario_data}

    @staticmethod
    def __dataframe_to_response(df):
        return list(map(Simulator.__dataframe_row_to_response, df.iterrows()))

    @staticmethod
    def __dataframe_row_to_response(index_row):
        row = index_row[1]
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
            "rEff": row.get("reff", None),
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

    def __reverse_map_scenario(self, scenario_index):
        with open(os.path.join(cl_path_prefix, self.parameters_directory,
                               "SCENARIO {}_params.json".format(scenario_index))) as params_file:
            covid_libscenario = json.load(params_file)
        phases = []
        phases.append(
            {
                "importedInfectionsPerDay": int(covid_libscenario["imported_infections_per_day"]),
                "trigger": date.today().isoformat(),
                "triggerType": covid_libscenario["trig_def_type"],
                "triggerCondition": covid_libscenario["trig_op_type"],
                "severity": float(covid_libscenario["severity"]),
                "proportionOfContactsTraced": float(covid_libscenario["prop_contacts_traced"]),
                "numTestsMitigation": int(covid_libscenario["num_tests_mitigation"]),
                "typeTestsMitigation": "PCR",
                "specificity": float(covid_libscenario["specificity"]),
                "sensitivity": float(covid_libscenario["sensitivity"]),
                "testingStrategy": covid_libscenario["test_strategy"],
                "numTestsCare": int(covid_libscenario["num_tests_care"]),
                "typeTestsCare": "PCR",
                "requiredDxTests": int(covid_libscenario["requireddxtests"])
            }
        )

        return {"phases": phases}

    def default_scenarios(self):
        return list(map(self.__reverse_map_scenario, range(0, 3)))
