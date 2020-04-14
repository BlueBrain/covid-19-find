import { apiBase } from './config';
import csv from 'csvtojson';
import { CountryParams } from './components/CountrySelector';

export type SimulationParams = {
  total_pop: number;
  pop_hospitals: number;
  pop_high_contact: number;
  prop_urban: number;
  prop_isolated: number;
  degraded: number;
  ge_65: number;
  prop_tests_hospitals: number;
  prop_tests_high_contact: number;
  prop_tests_rest_of_population: number;
  sensitivity_PCR: number;
  sensitivity_RDT: number;
  sensitivity_xray: number;
  selectivity_PCR: number;
  selectivity_RDT: number;
  selectivity_xray: number;
  num_tests_PCR: number;
  num_tests_RDT: number;
  num_tests_xray: number;
};

export type SimulationResponse = {
  scenarios: {
    maxInfected: number;
    maxIsolated: number;
    totalDeaths: number;
    totalTests: number;
    data: string;
  }[];
};

export type Scenarios = {
  maxInfected: number;
  maxIsolated: number;
  totalDeaths: number;
  totalTests: number;
  data: {
    beta: string;
    compartment: string;
    days: string;
    field1: string;
    new_tested: string;
    num_confirmed: string;
    num_deaths: string;
    num_infected: string;
    num_isolated: string;
    num_isolated_infected: string;
    num_recovered: string;
    population: string;
    susceptible_prop: string;
    susceptibles: string;
    tested: string;
    total_confirmed: string;
    total_deaths: string;
    total_infected: string;
    total_infected_notisolated: string;
    total_isolated: string;
    total_recovered: string;
  }[];
}[];

export type CountryResponse = {
  countryCode: string;
  highContactPopulation: number | null;
  hospitalBeds: number | null;
  hospitalEmployment: number | null;
  over65Percentage: number | null;
  population: number | null;
  remoteAreasPopulationPercentage: number | null;
  urbanPopulationInDegradedHousingPercentage: number | null;
  urbanPopulationPercentage: number | null;
};

export default class API {
  base: string;
  constructor() {
    this.base = apiBase;
  }

  countries() {
    return fetch(`${this.base}/countries`).then(response => response.json());
  }

  country(countryCode: string): Promise<CountryParams> {
    return fetch(`${this.base}/countries/${countryCode}`)
      .then(response => response.json())
      .then((response: CountryResponse) => {
        return {
          total_pop: response.population,
          pop_hospitals: response.hospitalEmployment,
          pop_high_contact: response.highContactPopulation,
          prop_urban: response.urbanPopulationPercentage,
          prop_isolated: response.remoteAreasPopulationPercentage,
          degraded: response.urbanPopulationInDegradedHousingPercentage,
          ge_65: response.over65Percentage,
          countryCode: response.countryCode,
          // TODO: reverse this and add these features
          // prop_tests_hospitals,
          // prop_tests_high_contact,
          // prop_tests_rest_of_population,
        };
      });
  }

  countryCovidData(countryCode: string) {
    return fetch(`${this.base}/covid19data/${countryCode}`).then(response =>
      response.json(),
    );
  }

  async simulation(simulationParams: SimulationParams): Promise<Scenarios> {
    const formData = new FormData();
    Object.keys(simulationParams).forEach(key => {
      formData.append(key, simulationParams[key]);
    });
    const response = await fetch(`${this.base}/simulation`, {
      method: 'POST',
      body: formData,
    });
    const simulationResponse: SimulationResponse = await response.json();
    const csvData = await Promise.all(
      simulationResponse.scenarios.map(scenario => {
        return csv().fromString(scenario.data);
      }),
    );
    return simulationResponse.scenarios.map((scenario, index) => {
      return {
        ...scenario,
        data: csvData[index],
      };
    });
  }
}
