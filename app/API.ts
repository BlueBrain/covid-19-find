import { apiBase, DEFAULT_SCENARIO_LABELS } from './config';
import { CountryResponse } from './types/country';
import {
  SimulationResults,
  Scenario,
  Phase,
  ClientSimulationRequest,
  TRIGGER_TYPE,
} from './types/simulation';
import { toLetters } from './libs/strings';
import { match, when } from 'ts-pattern';

export const INVALID_SCORE_THRESHOLD = 0.45;

export const isScoreInvalid = (score: number) =>
  score > INVALID_SCORE_THRESHOLD;

const fixPhases = (phase: Phase, index: number) => ({
  ...phase,
  name: index === 0 ? 'Current Phase' : 'Next Phase',
  fatalityReductionRecent: phase.fatalityReductionRecent * 100,
});

const fixScenario = (scenario: Scenario, index: number) => ({
  name: match(index)
    .with(
      when(index => index <= DEFAULT_SCENARIO_LABELS.length - 1),
      index => DEFAULT_SCENARIO_LABELS[index],
    )
    .otherwise(() => `Scenario ${toLetters(index).toLocaleUpperCase()}`),
  phases: scenario.phases.map(fixPhases),
});

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
          scenarios: data.scenarios.map(fixScenario),
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
        fatalityReduction: response.fatalityReduction
          ? Number((response.fatalityReduction * 100).toFixed(2))
          : null,
      }));
  }

  countryCovidData(countryCode: string) {
    return fetch(`${this.base}/covid19data/${countryCode}`).then(response =>
      response.json(),
    );
  }

  async simulation(
    simulationParams: ClientSimulationRequest,
  ): Promise<SimulationResults> {
    const formattedParams = {
      ...simulationParams,
      scenarios: simulationParams.scenarios.map(scenario => ({
        phases: scenario.phases.map(
          ({
            name,
            fatalityReductionRecent,
            trigger,
            triggerType,
            ...rest
          }) => {
            return {
              ...rest,
              fatalityReductionRecent: fatalityReductionRecent / 100,
              triggerType,
              // Some trigger types should be percentages
              // https://github.com/BlueBrain/covid-19-find/issues/201
              trigger: match<string, string | number>(triggerType)
                .with(TRIGGER_TYPE.POSITIVES, () => Number(trigger) / 100)
                .with(TRIGGER_TYPE.INCREASE_CASES, () => Number(trigger) / 100)
                .with(TRIGGER_TYPE.INCREASE_DEATHS, () => Number(trigger) / 100)
                .otherwise(() => `${trigger}`),
            };
          },
        ),
      })),
      population: Number(simulationParams.population),
      urbanPopulationProportion:
        simulationParams.urbanPopulationProportion / 100,
      belowPovertyLineProportion:
        simulationParams.belowPovertyLineProportion / 100,
      workingOutsideHomeProportion:
        simulationParams.workingOutsideHomeProportion / 100,
      activePopulationProportion:
        simulationParams.activePopulationProportion / 100,
      over64Proportion: simulationParams.over64Proportion / 100,
      fatalityReduction: simulationParams.fatalityReduction / 100,
    };

    const response = await fetch(`${this.base}/simulation`, {
      method: 'POST',
      body: JSON.stringify(formattedParams),
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const simulationResults = (await response.json()) as SimulationResults;
    return simulationResults;
  }
}
