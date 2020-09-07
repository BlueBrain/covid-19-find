import { takeRight } from 'lodash';

import { apiBase } from './config';
import { CountryResponse } from './types/country';
import {
  SimulationRequest,
  SimulationResults,
  Scenario,
} from './types/simulation';

export default class API {
  base: string;
  constructor() {
    this.base = apiBase;
  }

  countries() {
    return fetch(`${this.base}/countries`).then(response => response.json());
  }

  scenarios() {
    return (
      fetch(`${this.base}/scenarios`)
        .then(response => response.json())
        // TODO: remove this when default scenarios are created dynamically
        .then((data: { scenarios: Scenario[] }) => ({
          scenarios: data.scenarios.map(scenario => ({
            phases: takeRight(scenario.phases, 2),
          })),
        }))
    );
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

  async simulation(
    simulationParams: SimulationRequest,
  ): Promise<SimulationResults> {
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
    };

    const response = await fetch(`${this.base}/simulation`, {
      method: 'POST',
      body: JSON.stringify(formattedParams),
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const simulationResults = await response.json();
    return simulationResults as SimulationResults;
  }
}
