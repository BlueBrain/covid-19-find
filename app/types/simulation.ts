export enum TRIGGER_TYPE {
  DATE = 'date',
  DEATHS = 'deaths',
  CASES = 'cases',
  INCREASE_DEATHS = 'increase deaths',
  INCREASE_CASES = 'increase cases',
  POSITIVES = 'positives',
  CASES_PER_MILLSION = 'cases per million',
}

export enum TRIGGER_CONDITION {
  EQUAL = '=',
  LESS_THAN = '<',
  GREATER_OR_EQUAL = '>=',
}

export enum TEST_TYPES {
  PCR = 'PCR',
  RDT = 'RDT',
}

export enum TESTING_STRATEGIES {
  NONE = 'no testing',
  ALL = 'all symptomatic',
  SPECIAL = 'special groups with symptoms',
  OPEN = 'open public testing',
}

export type CountryData = {
  countryCode: string;
  population: number;
  activePopulationProportion: number;
  hospitalBeds: number;
  hospitalStaffPerBed: number;
  workingOutsideHomeProportion: number;
  urbanPopulationProportion: number;
  over64Proportion: number;
  belowPovertyLineProportion: number;
  fatalityReduction: number;
};

export type Phase = {
  testingStrategy: TESTING_STRATEGIES;
  importedInfectionsPerDay: number;
  trigger: string;
  triggerType: string;
  triggerCondition: string;
  severity: number;
  proportionOfContactsTraced: number;
  numTestsMitigation: number;
  typeTestsMitigation: TEST_TYPES;
  confirmationTests: boolean;
  specificity: number;
  sensitivity: number;
  testSymptomaticOnly: boolean;
  numTestsCare: number;
  typeTestsCare: TEST_TYPES;
  requiredDxTests: number;
  resultPeriod: number;
  fatalityReductionRecent: number;
};

export type ClientPhase = Phase & {
  name: string;
};

export type Scenario = {
  phases: Phase[];
};

export type ClientScenarioData = {
  name: string;
  phases: ClientPhase[];
};

export type ClientSimulationRequest = CountryData & {
  scenarios: ClientScenarioData[];
};

export type SimulationRequest = CountryData & {
  scenarios: Scenario[];
};

export type SimulationResults = {
  scenarios: ScenarioResult[];
};

export type TestingImpact = {
  tests: number;
  livesSaved: number;
  rEff: number;
};

export type ScenarioResult = {
  data: {
    hospitals: ScenarioResultDatasetTimeSeries[];
    otherHighContact: ScenarioResultDatasetTimeSeries[];
    restOfPopulation: ScenarioResultDatasetTimeSeries[];
    total: ScenarioResultDatasetTimeSeries[];
  };
  testingImpact: TestingImpact[];
  maxInfected: number;
  maxIsolated: number;
  totalDeaths: number;
  totalInfected: number;
  totalTests: number;
};

export type ScenarioResultDatasetTimeSeries = {
  actualDxTest: number;
  beta: number;
  currentInfected: number;
  currentInfectedNotIsolated: number;
  currentIsolated: number;
  date: string;
  day: number;
  detectionRate: null;
  falseNegatives: number;
  falsePositives: number;
  incidence: number;
  newConfirmed: number;
  newDeaths: number;
  newInfected: number;
  newIsolated: number;
  newIsolatedInfected: number;
  newRecovered: number;
  newTests: number;
  newTestsPositiveProportion: null;
  npv: number;
  population: number;
  ppv: number;
  prevalence: number;
  rEff: null;
  requiredDxTests: number;
  susceptibleProportion: number;
  susceptibles: number;
  totalConfirmed: number;
  totalDeaths: number;
  totalInfected: number;
  totalRecovered: number;
  totalTested: number;
  trueNegatives: number;
  truePositives: number;
};
