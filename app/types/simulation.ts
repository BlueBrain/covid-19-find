export enum TRIGGER_TYPE {
  DATE = 'date',
  DEATHS = 'deaths',
  CASES = 'cases',
  INCREASE_DEATHS = 'increase deaths',
  INCREASE_CASES = 'increase cases',
  POSITIVES = 'positives',
  CASES_PER_MILLSION = 'cases per million',
}

export const triggerTypeLabels = {
  [TRIGGER_TYPE.DATE]: 'Date',
  [TRIGGER_TYPE.DEATHS]: 'Deaths',
  [TRIGGER_TYPE.CASES]: 'Cases',
  [TRIGGER_TYPE.INCREASE_DEATHS]: 'Increased Deaths (%)',
  [TRIGGER_TYPE.INCREASE_CASES]: 'Increased Cases (%)',
  [TRIGGER_TYPE.POSITIVES]: 'Positives (%)',
  [TRIGGER_TYPE.CASES_PER_MILLSION]: 'Cases per million',
};

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
  HIGH_CONTACT_FIRST = 'high contact groups first',
  SYMPOMATIC_FIRST = 'symptomatic first',
  OPEN = 'open public testing',
}

export enum IMPORTED_INFECTIONS {
  HIGHLY_EFFECTIVE = 'highly effective',
  FAIRLY_EFFECTIVE = 'fairly effective',
  NOT_EFFECTIVE = 'not effective',
}

export enum CONTACT_TRACING {
  NONE = 'none',
  HIGHLY_EFFECTIVE = 'highly effective',
  FAIRLY_EFFECTIVE = 'fairly effective',
}

export const ImportedInfectionLabels = {
  [IMPORTED_INFECTIONS.HIGHLY_EFFECTIVE]: 'Highly Effective',
  [IMPORTED_INFECTIONS.FAIRLY_EFFECTIVE]: 'Fairly Effective',
  [IMPORTED_INFECTIONS.NOT_EFFECTIVE]: 'Not Effective',
};

export const ContractTracingLabels = {
  [CONTACT_TRACING.NONE]: 'None',
  [CONTACT_TRACING.FAIRLY_EFFECTIVE]: 'Fairly Effective',
  [CONTACT_TRACING.HIGHLY_EFFECTIVE]: 'Highly Effective',
};

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
  trigger: string | number;
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
  resultsPeriod: number;
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
  score: number;
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
  testsNeededForCare: number;
  testsNeededForMitigation: number;
  totalPositiveTests: number;
  samplesRequiredForSerologicalStudies: {
    numSubgroups: number;
    testsRequired: number;
  }[];
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
