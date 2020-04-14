import { apiBase } from './config';
import csv from 'csvtojson';

export type SimulationParams = {
  population: number;
  hospitalBeds: number;
  highContactPopulation: number;
  urbanPopulationProportion: number;
  remoteAreasPopulationProportion: number;
  urbanPopulationInDegradedHousingProportion: number;
  over65Proportion: number;
  hospitalTestsProportion: number;
  highContactTestsProportion: number;
  restOfPopulationTestsProportion: number;
  hospitalEmployment: number | null; // TODO: change this because model doesnt use it
  sensitivityPCR: number;
  sensitivityRDT: number;
  sensitivityXray: number;
  specificityPCR: number;
  specificityRDT: number;
  specificityXray: number;
  numTestsPCR: number;
  numTestsRDT: number;
  numTestsXray: number;
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
  over65Proportion: number | null;
  population: number | null;
  remoteAreasPopulationProportion: number | null;
  urbanPopulationInDegradedHousingProportion: number | null;
  urbanPopulationProportion: number | null;
};

export default class API {
  base: string;
  constructor() {
    this.base = apiBase;
  }

  countries() {
    return fetch(`${this.base}/countries`).then(response => response.json());
  }

  country(countryCode: string): Promise<CountryResponse> {
    return fetch(`${this.base}/countries/${countryCode}`).then(response =>
      response.json(),
    );
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
