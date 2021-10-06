import { DEFAULT_SCENARIO_LABELS } from '../../config';
import {
  TRIGGER_TYPE,
  TRIGGER_CONDITION,
  TESTING_STRATEGIES,
  triggerTypeLabels,
  IMPORTED_INFECTIONS,
  ImportedInfectionLabels,
  CONTACT_TRACING,
  ContractTracingLabels,
  EFFECTIVENESS,
  EffectivenessLabels,
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
        label: 'Stringency',
        type: INPUT_TYPES.select,
        options: Object.values(EFFECTIVENESS).map(str => ({
          label: EffectivenessLabels[str],
          value: str,
        })),
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
        options: Object.values(CONTACT_TRACING).map(str => ({
          label: ContractTracingLabels[str],
          value: str,
        })),
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
        label: 'Symptoms to result (days)',
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
  
] as {
  title: string;
  input: AnyInputProp[];
}[];
