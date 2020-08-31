from .simulation.covidlib import run_simulation, get_scenarios
import numpy as np
import math
import pandas as pd


class Simulator:
    SIMULATION_DAYS = 186

    def __init__(self, covid_repository):
        self.covid_repository = covid_repository

    @staticmethod
    def __map_datapoint(dp):
        return {
            "Date": dp["date"],
            "accumulated_deaths": dp["totalDeaths"],
            "accumulated_cases": dp["totalConfirmed"],
            "tests": dp["newTests"]
        }

    def get_country_df(self, country_code):
        covid_data = self.covid_repository.data_for(country_code)["timeseries"][:self.SIMULATION_DAYS]
        return pd.DataFrame.from_records(list(map(self.__map_datapoint, covid_data)))

    @staticmethod
    def get_fixed_parameters(parameters):
        return {
            "total_pop": parameters["population"],
            "hospital_beds": parameters["hospitalBeds"],
            "prop_15_64": parameters["activePopulationProportion"],
            "age_gt_64": parameters["over64Proportion"],
            "prop_urban": parameters["urbanPopulationProportion"],
            "prop_below_pl": parameters["belowPovertyLineProportion"],
            "prop_woh": parameters["workingOutsideHomeProportion"],
            "staff_per_bed": parameters["hospitalStaffPerBed"]
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
            "sensitivity": Simulator.__get_array_for_key(phases, "sensitivity"),
            "specificity": Simulator.__get_array_for_key(phases, "specificity"),
            "symptomatic_only": Simulator.__get_array_for_key(phases, "testSymptomaticOnly", str),
            "confirmation_tests": Simulator.__get_array_for_key(phases, "confirmationTests", str),
            "prop_hospital": Simulator.__get_array_for_key(phases, "hospitalTestProportion"),
            "prop_other_hc": Simulator.__get_array_for_key(phases, "otherHighContactPopulationTestProportion"),
            "prop_rop": Simulator.__get_array_for_key(phases, "restOfPopulationTestProportion"),
            "test_multipliers": [0, 1, 2, 3],
            "num_tests_care": Simulator.__get_array_for_key(phases, "numTestsCare"),
            "type_tests_care": Simulator.__get_array_for_key(phases, "typeTestsCare"),
            "requireddxtests": Simulator.__get_array_for_key(phases, "requiredDxTests")
        }

    @staticmethod
    def __get_array_for_key(scenarios, key, func=lambda x: x):
        return list(map(lambda scenario: func(scenario[key]), scenarios))

    def run(self, parameters):
        scenarios = self.get_scenario_parameters(parameters)
        country_df = self.get_country_df(parameters["countryCode"])
        print(country_df.iloc[55])
        result = run_simulation(country_df, self.get_fixed_parameters(parameters), scenarios=scenarios)

        scenario_data = []
        scenario_dfs = result[0]
        scenario_totals = result[2]
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
                    }
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

    @staticmethod
    def __reverse_map_scenario(covidlib_scenario):
        if covidlib_scenario["symptomatic_only"].lower() == "true":
            test_symptomatic_only = True
        elif covidlib_scenario["symptomatic_only"].lower() == "false":
            test_symptomatic_only = False
        else:
            test_symptomatic_only = None
        return {
            "interventionType": Simulator.REVERSE_INTERVENTION_PARAMS[int(covidlib_scenario["intervention_type"])],
            "interventionTiming": Simulator.REVERSE_TIMING_PARAMS[int(covidlib_scenario["intervention_timing"])],
            "testSymptomaticOnly": test_symptomatic_only,
            "hospitalTestProportion": covidlib_scenario["prop_hospitals"],
            "otherHighContactPopulationTestProportion": covidlib_scenario["prop_other_hc"],
            "restOfPopulationTestProportion": 1 - covidlib_scenario["prop_hospitals"] - covidlib_scenario[
                "prop_other_hc"]
        }

    def default_scenarios(self):
        return list(map(Simulator.__reverse_map_scenario, getscenarios()))
