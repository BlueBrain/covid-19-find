export enum TEST_TYPES {
  PCR = 'PCR',
  RDT = 'RDT',
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
};

export type Phase = {
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
  hospitalTestProportion: number;
  otherHighContactPopulationTestProportion: number;
  restOfPopulationTestProportion: number;
  numTestsCare: number;
  typeTestsCare: TEST_TYPES;
  requiredDxTests: number;
};

export type Scenario = {
  phases: Phase[];
};

export type ClientScenarioData = {
  name: string;
  phases: Phase[];
};

export type SimulationRequest = CountryData & {
  scenarios: Scenario[];
};

export type SimulationResults = {};
