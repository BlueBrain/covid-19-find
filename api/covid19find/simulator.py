from .simulation.covidlib import run_simulation, getscenarios


class Simulator:
    TIMING_PARAMS = {
        ">1": 0,
        ">5": 1,
        ">10": 2,
        ">20": 3,
        ">50": 4,
        "never": 5,
    }
    INTERVENTION_PARAMS = {
        "no_intervention": 0,
        "mild_intervention": 1,
        "lockdown": 2
    }

    REVERSE_TIMING_PARAMS = {v: k for k, v in TIMING_PARAMS.items()}
    REVERSE_INTERVENTION_PARAMS = {v: k for k, v in INTERVENTION_PARAMS.items()}

    @staticmethod
    def get_fixed_parameters(parameters):
        return {
            "total_pop": parameters["population"],
            "hospital_beds": parameters["hospitalBeds"],
            "prop_15_64": parameters["activePopulationProportion"],
            "prop_urban": parameters["urbanPopulationProportion"],
            "prop_below_pl": parameters["belowPovertyLineProportion"],
            "prop_woh": parameters["workingOutsideHomeProportion"],
            "staff_per_bed": parameters["hospitalStaffPerBed"],
            "sensitivity_PCR": parameters["sensitivityPCR"],
            "sensitivity_RDT": parameters["sensitivityRDT"],
            "sensitivity_xray": parameters["sensitivityXray"],
            "specificity_PCR": parameters["specificityPCR"],
            "specificity_RDT": parameters["specificityRDT"],
            "specificity_xray": parameters["specificityXray"],
            "num_tests_PCR": parameters["numTestsPCR"],
            "num_tests_RDT": parameters["numTestsRDT"],
            "num_tests_xray": parameters["numTestsXray"]
        }

    @staticmethod
    def get_scenario_parameters(parameters):
        if "scenarios" in parameters:
            return list(map(Simulator.__map_scenario, parameters["scenarios"]))
        else:
            return None

    @staticmethod
    def __map_scenario(input_scenario):
        return {
            "intervention_type": Simulator.INTERVENTION_PARAMS[input_scenario["interventionType"]],
            "intervention_timing": Simulator.TIMING_PARAMS[input_scenario["interventionTiming"]],
            "symptomatic_only": str(input_scenario["testSymptomaticOnly"]),
            "prop_hospital": input_scenario["hospitalTestProportion"],
            "prop_other_hc": input_scenario["otherHighContactPopulationTestProportion"],
            "prop_rop": 1 - input_scenario["hospitalTestProportion"] - input_scenario[
                "otherHighContactPopulationTestProportion"]
        }

    def run(self, parameters):
        scenarios = self.get_scenario_parameters(parameters)
        if scenarios is not None:
            result = run_simulation(self.get_fixed_parameters(parameters), scenarios=scenarios)
        else:
            result = run_simulation(self.get_fixed_parameters(parameters))

        scenario_data = []
        scenario_dfs = result[0]
        scenario_total_tests = result[1]
        scenario_total_deaths = result[2]
        scenario_max_infected = result[3]
        scenario_max_isolated = result[4]
        for i in range(0, len(scenario_dfs)):
            scenario_data.append(
                {
                    "data": scenario_dfs[i].to_csv(),
                    "totalTests": scenario_total_tests[i],
                    "totalDeaths": scenario_total_deaths[i],
                    "maxInfected": scenario_max_infected[i],
                    "maxIsolated": scenario_max_isolated[i]
                }
            )
        return scenario_data

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
