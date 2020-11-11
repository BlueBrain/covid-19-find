import { ClientScenarioData } from './types/simulation';

export const DEFAULT_SCENARIO_LIST: ClientScenarioData[] = [
  {
    name: 'Counterfactual: No tests and no intervention',
    phases: [],
  },
];

export const DEFAULT_SIMULATION_REQUEST_PARAMS = {
  countryCode: null,
  population: null,
  hospitalBeds: null,
  workingOutsideHomeProportion: null,
  urbanPopulationProportion: null,
  hospitalStaffPerBed: 2.5,
  activePopulationProportion: null,
  belowPovertyLineProportion: null,
  fatalityReduction: 0.5,
  hospitalEmployment: null,
  over64Proportion: null,
  sensitivityPCR: 0.95,
  sensitivityRDT: 0.85,
  sensitivityXray: 0,
  specificityPCR: 0.95,
  specificityRDT: 0.9,
  specificityXray: 0,
  numTestsPCR: 1000,
  numTestsRDT: 1000,
  numTestsXray: 0,
  scenarios: DEFAULT_SCENARIO_LIST,
};
