from .simulation.covidlib import run_simulation
from io import StringIO


class Simulator:

    def run(self, total_pop, pop_hospitals, pop_high_contact, prop_urban, prop_isolated, degraded, ge_65,
            prop_tests_hospitals, prop_tests_high_contact, prop_tests_rest_of_population, sensitivity_PCR,
            sensitivity_RDT, sensitivity_xray, selectivity_PCR, selectivity_RDT, selectivity_xray,
            num_tests_PCR, num_tests_RDT, num_tests_xray):
        result = run_simulation(total_pop, pop_hospitals, pop_high_contact, prop_urban, prop_isolated, degraded, ge_65,
                                prop_tests_hospitals, prop_tests_high_contact, prop_tests_rest_of_population,
                                sensitivity_PCR,
                                sensitivity_RDT, sensitivity_xray, selectivity_PCR, selectivity_RDT, selectivity_xray,
                                num_tests_PCR, num_tests_RDT, num_tests_xray)
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
