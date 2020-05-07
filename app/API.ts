import { apiBase } from './config';
import csv from 'csvtojson';

export enum InterventionType {
  NONE = 'no_intervention',
  MILD = 'mild_intervention',
  LOCKDOWN = 'lockdown',
}

export enum InterventionTiming {
  NEVER = 'never',
  VERY_EARLY = 'very_early',
  EARLY = 'early',
  LATE = 'late',
  VERY_LATE = 'very_late',
}

export const DEFAULT_SCENARIO_LIST: Scenario[] = [
  {
    name: 'Baseline',
    interventionType: InterventionType.LOCKDOWN,
    description:
      'This imaginary scenario is provided for comparison purposes. It shows the predicted course of the pandemic with a strong lockdown but no testing of any kind.',
    interventionTiming: InterventionTiming.LATE,
    testSymptomaticOnly: true,
    hospitalTestProportion: 0,
    otherHighContactPopulationTestProportion: 0,
  },
  {
    name: 'Identify and isolate positive cases',
    interventionType: InterventionType.LOCKDOWN,
    description:
      'This scenario models the potential outcomes of a testing strategy that aims to identify and isolate the highest possible number of infected people, slowing the spread of the disease. The scenario presupposes a strong lockdown. It assumes that 50% of available tests are used to test hospital staff and 50% are used for other groups at high risk of contracting or transmitting the infection (e.g. shopkeepers, police, factory and transport workers who have a high level of contact with the public, and people living below the poverty line in large cities).  Tests are performed only on people showing symptoms. ',
    interventionTiming: InterventionTiming.LATE,
    testSymptomaticOnly: true,
    hospitalTestProportion: 50,
    otherHighContactPopulationTestProportion: 50,
  },
  {
    name: 'Protect hospital resources',
    interventionType: InterventionType.LOCKDOWN,
    description:
      'This scenario models the potential outcomes of a testing strategy that aims to reduce the burden of the pandemic on hospital staff, preserving the capabilities necessary to help others. The scenario presupposes a strong lockdown. It assumes that all available tests are used to test hospital staff, if possible repeatedly. Tests are performed only on people showing symptoms.',
    interventionTiming: InterventionTiming.LATE,
    testSymptomaticOnly: true,
    hospitalTestProportion: 100,
    otherHighContactPopulationTestProportion: 0,
  },
];

export type Scenario = {
  name: string;
  description: string;
  interventionType: InterventionType;
  interventionTiming: InterventionTiming;
  testSymptomaticOnly: boolean;
  hospitalTestProportion: number;
  otherHighContactPopulationTestProportion: number;
};

export type SimulationParams = {
  population: number;
  hospitalBeds: number;
  workingOutsideHomeProportion: number;
  urbanPopulationProportion: number;
  hospitalStaffPerBed: number;
  activePopulationProportion: number;
  belowPovertyLineProportion: number;
  over64Proportion: number;
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
  scenarios: Scenario[];
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
  over64Proportion: number | null;
  population: number | null;
  remoteAreasPopulationProportion: number | null;
  belowPovertyLineProportion: number | null;
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

  scenarios() {
    return fetch(`${this.base}/scenarios`).then(response => response.json());
  }

  country(countryCode: string): Promise<CountryResponse> {
    return fetch(`${this.base}/countries/${countryCode}`)
      .then(response => response.json())
      .then(response => ({
        ...response,
        urbanPopulationProportion: response.urbanPopulationProportion
          ? Number((response.urbanPopulationProportion * 100).toFixed(2))
          : null,
        activePopulationProportion: response.activePopulationProportion
          ? Number((response.activePopulationProportion * 100).toFixed(2))
          : null,
        over64Proportion: response.over64Proportion
          ? Number((response.over64Proportion * 100).toFixed(2))
          : null,
      }));
  }

  countryCovidData(countryCode: string) {
    return fetch(`${this.base}/covid19data/${countryCode}`).then(response =>
      response.json(),
    );
  }

  async simulation(simulationParams: SimulationParams): Promise<Scenarios> {
    const formattedParams = {
      ...simulationParams,
      urbanPopulationProportion:
        simulationParams.urbanPopulationProportion / 100,
      belowPovertyLineProportion:
        simulationParams.belowPovertyLineProportion / 100,
      workingOutsideHomeProportion:
        simulationParams.workingOutsideHomeProportion / 100,
      activePopulationProportion:
        simulationParams.activePopulationProportion / 100,
      over64Proportion: simulationParams.over64Proportion / 100,
      scenarios: simulationParams.scenarios.map(scenario => {
        return {
          ...scenario,
          hospitalTestProportion: scenario.hospitalTestProportion / 100,
          otherHighContactPopulationTestProportion:
            scenario.otherHighContactPopulationTestProportion / 100,
          testSymptomaticOnly: !!scenario.testSymptomaticOnly,
        };
      }),
    };

    const typedParams = {
      ...formattedParams,
      ...Object.keys(formattedParams)
        .filter(key => key !== 'countryCode' && key !== 'scenarios')
        .reduce((memo, key) => {
          memo[key] = Number(memo[key]);
          return memo;
        }, formattedParams),
    };

    const response = await fetch(`${this.base}/simulation`, {
      method: 'POST',
      body: JSON.stringify(typedParams),
      headers: {
        'Content-Type': 'application/json',
      },
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
