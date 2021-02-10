import { DEFAULT_SCENARIO_LABELS } from '../../config';
import {
  TRIGGER_TYPE,
  TRIGGER_CONDITION,
  TESTING_STRATEGIES,
  triggerTypeLabels,
  IMPORTED_INFECTIONS,
  ImportedInfectionLabels,
} from '../../types/simulation';

export enum INPUT_TYPES {
  number = 'number',
  select = 'select',
  boolean = 'boolean',
  text = 'text',
}

export type InputProp = {
  label: string;
  type: INPUT_TYPES;
  key: string;
  disabled?: boolean;
  required?: boolean;
  name?: string;
};

export type NumberInputProp = InputProp & {
  type: INPUT_TYPES.number;
  min?: number;
  max?: number;
  step?: number;
  validation?: {
    type: 'equals';
    value: number;
    keysToMatch: string[];
  };
};

export type SelectInputProp = InputProp & {
  type: INPUT_TYPES.select;
  options: {
    value: string | null;
    label: string;
  }[];
};

export type BooleanInputProp = InputProp & {
  type: INPUT_TYPES.boolean;
};

export type AnyInputProp = SelectInputProp | BooleanInputProp | NumberInputProp;

export enum TEST_TYPES {
  PCR = 'PCR',
  RDT = 'RDT',
}

export default [
  {
    title: 'Government Intervention',
    input: [
      {
        label: 'Trigger Type',
        type: INPUT_TYPES.select,
        key: 'triggerType',
        options: Object.values(TRIGGER_TYPE).map(str => ({
          label: triggerTypeLabels[str],
          value: str,
        })),
      },
      {
        label: 'Trigger Condition',
        type: INPUT_TYPES.select,
        key: 'triggerCondition',
        options: Object.values(TRIGGER_CONDITION).map(str => ({
          label: str,
          value: str,
        })),
      },
      {
        label: 'Trigger Value',
        type: INPUT_TYPES.text,
        key: 'trigger',
      },
      {
        label: 'Effectiveness',
        type: INPUT_TYPES.number,
        min: 0,
        max: 1,
        step: 0.01,
        key: 'severity',
      },
      {
        label: 'Border controls',
        type: INPUT_TYPES.select,
        key: 'importedInfectionsPerDay',
        options: Object.values(IMPORTED_INFECTIONS).map(str => ({
          label: ImportedInfectionLabels[str],
          value: str,
        })),
      },
    ],
  },
  {
    title: 'Contact Tracing',
    input: [
      {
        label: 'Trace and isolate contacts',
        type: INPUT_TYPES.select,
        key: 'proportionOfContactsTraced',
        options: [
          {
            label: 'None',
            value: 0,
          },
          {
            label: '10%',
            value: 0.1,
          },
          {
            label: '20%',
            value: 0.2,
          },
          {
            label: '25%',
            value: 0.25,
          },
          {
            label: '50%',
            value: 0.5,
          },
        ],
      },
    ],
  },
  {
    title: 'Testing for Mitigation',
    input: [
      {
        label: 'Testing Strategy',
        type: INPUT_TYPES.select,
        min: 0,
        key: 'testingStrategy',
        options: Object.values(TESTING_STRATEGIES).map((str, index) => ({
          label: DEFAULT_SCENARIO_LABELS[index],
          value: str,
        })),
      },
      {
        label: 'Number of tests per day',
        type: INPUT_TYPES.number,
        min: 0,
        key: 'numTestsMitigation',
      },
      {
        label: 'Test Type',
        type: INPUT_TYPES.select,
        min: 0,
        key: 'typeTestsMitigation',
        options: [
          {
            label: TEST_TYPES.PCR,
            value: TEST_TYPES.PCR,
          },
          {
            label: TEST_TYPES.RDT,
            value: TEST_TYPES.RDT,
          },
        ],
      },
      {
        label: 'Sensitivity',
        type: INPUT_TYPES.number,
        min: 0,
        max: 1,
        step: 0.01,
        key: 'sensitivity',
      },
      {
        label: 'Specificity',
        type: INPUT_TYPES.number,
        min: 0,
        max: 1,
        step: 0.001,
        key: 'specificity',
      },
      {
        label: 'Time to result',
        type: INPUT_TYPES.number,
        min: 0,
        max: 30,
        step: 1,
        key: 'resultsPeriod',
      },
      {
        label:
          'Estimated reduction in infection fatality rate (IFR) since start of epidemic (%)',
        type: INPUT_TYPES.number,
        min: 0,
        max: 100,
        step: 0.1,
        key: 'fatalityReductionRecent',
      },
    ],
  },
  {
    title: 'Testing for Care',
    input: [
      {
        label: 'Test Type',
        type: INPUT_TYPES.select,
        min: 0,
        key: 'typeTestsCare',
        options: [
          {
            label: TEST_TYPES.PCR,
            value: TEST_TYPES.PCR,
          },
          {
            label: TEST_TYPES.RDT,
            value: TEST_TYPES.RDT,
          },
        ],
      },
      {
        label: 'Total tests per day',
        type: INPUT_TYPES.number,
        min: 0,
        key: 'numTestsCare',
      },
      {
        label: 'Recommended number of tests for care of one patient',
        type: INPUT_TYPES.number,
        min: 0,
        key: 'requiredDxTests',
      },
    ],
  },
] as {
  title: string;
  input: AnyInputProp[];
}[];
