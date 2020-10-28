import moment from 'moment';
import {
  ClientScenarioData,
  TESTING_STRATEGIES,
  TEST_TYPES,
} from './types/simulation';

export const DEFAULT_SCENARIO_LIST: ClientScenarioData[] = [
  {
    name: 'Counterfactual: No tests and no intervention',
    phases: [
      {
        name: 'Current Phase',
        importedInfectionsPerDay: 20,
        trigger: moment(Date.now()).format('YYYY-MM-DD'),
        triggerType: 'date',
        triggerCondition: '>=',
        severity: 0.8,
        proportionOfContactsTraced: 0.25,
        numTestsMitigation: 1000,
        typeTestsMitigation: TEST_TYPES.PCR,
        specificity: 0.95,
        sensitivity: 0.95,
        testSymptomaticOnly: true,
        confirmationTests: true,
        // hospitalTestProportion: 0.5,
        // otherHighContactPopulationTestProportion: 0.5,
        // restOfPopulationTestProportion: 0,
        numTestsCare: 1000,
        typeTestsCare: TEST_TYPES.PCR,
        requiredDxTests: 1,
        testingStrategy: TESTING_STRATEGIES.NONE,
        resultPeriod: 5,
        proportionAsymptomaticTested: 0.01,
      },
      {
        name: 'Next Phase',
        importedInfectionsPerDay: 30,
        trigger: moment(Date.now()).format('YYYY-MM-DD'),
        triggerType: 'date',
        triggerCondition: '>=',
        severity: 0.6,
        proportionOfContactsTraced: 0.5,
        numTestsMitigation: 1000,
        typeTestsMitigation: TEST_TYPES.PCR,
        specificity: 0.95,
        sensitivity: 0.95,
        testSymptomaticOnly: true,
        confirmationTests: true,
        // hospitalTestProportion: 0.5,
        // otherHighContactPopulationTestProportion: 0.5,
        // restOfPopulationTestProportion: 0,
        numTestsCare: 1000,
        typeTestsCare: TEST_TYPES.PCR,
        requiredDxTests: 1,
        testingStrategy: TESTING_STRATEGIES.NONE,
        resultPeriod: 5,
        proportionAsymptomaticTested: 0.01,
      },
    ],
  },
  // TODO: how shall default phases look like?
  // {
  //   name: 'Identify and isolate positive cases',
  //   phases: [],
  // },
  // {
  //   name: 'Protect hospital resources',
  //   phases: [],
  // },
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
