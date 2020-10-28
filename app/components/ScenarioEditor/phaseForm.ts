import {
  TRIGGER_TYPE,
  TRIGGER_CONDITION,
  TESTING_STRATEGIES,
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
    title: 'Epidemic',
    input: [
      {
        label: 'Imported infections per day',
        type: INPUT_TYPES.number,
        min: 0,
        key: 'importedInfectionsPerDay',
      },
    ],
  },
  {
    title: 'Government Intervention',
    input: [
      {
        label: 'Trigger Type',
        type: INPUT_TYPES.select,
        key: 'triggerType',
        options: [
          {
            label: TRIGGER_TYPE.DATE,
            value: TRIGGER_TYPE.DATE,
          },
          {
            label: TRIGGER_TYPE.CASES,
            value: TRIGGER_TYPE.CASES,
          },
          {
            label: TRIGGER_TYPE.DEATHS,
            value: TRIGGER_TYPE.DEATHS,
          },
          {
            label: TRIGGER_TYPE.POSITIVES,
            value: TRIGGER_TYPE.POSITIVES,
          },
          {
            label: TRIGGER_TYPE.INCREASE_CASES,
            value: TRIGGER_TYPE.INCREASE_CASES,
          },
          {
            label: TRIGGER_TYPE.INCREASE_DEATHS,
            value: TRIGGER_TYPE.INCREASE_DEATHS,
          },
        ],
      },
      {
        label: 'Trigger Condition',
        type: INPUT_TYPES.select,
        key: 'triggerCondition',
        options: [
          {
            label: TRIGGER_CONDITION.EQUAL,
            value: TRIGGER_CONDITION.EQUAL,
          },
          {
            label: TRIGGER_CONDITION.LESS_THAN,
            value: TRIGGER_CONDITION.LESS_THAN,
          },
          {
            label: TRIGGER_CONDITION.GREATER_OR_EQUAL,
            value: TRIGGER_CONDITION.GREATER_OR_EQUAL,
          },
        ],
      },
      {
        label: 'Trigger Value',
        type: INPUT_TYPES.text,
        key: 'trigger',
      },
      {
        label: 'Severity',
        type: INPUT_TYPES.number,
        min: 0,
        max: 1,
        step: 0.01,
        key: 'severity',
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
            value: null,
          },
          {
            label: '10%',
            value: 0.1,
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
        options: [
          {
            label: TESTING_STRATEGIES.ALL,
            value: TESTING_STRATEGIES.ALL,
          },
          {
            label: TESTING_STRATEGIES.OPEN,
            value: TESTING_STRATEGIES.OPEN,
          },
          {
            label: TESTING_STRATEGIES.SPECIAL,
            value: TESTING_STRATEGIES.SPECIAL,
          },
        ],
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
            label: 'None',
            value: null,
          },
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
        step: 0.01,
        key: 'specificity',
      },
      {
        label: 'Time to result',
        type: INPUT_TYPES.number,
        min: 0,
        max: 30,
        step: 1,
        key: 'resultPeriod',
      },
      {
        label: 'Proportion asymptomatic tested per day',
        type: INPUT_TYPES.number,
        min: 0,
        max: 1,
        step: 0.01,
        key: 'proportionAsymptomaticTested',
      },
      // {
      //   label: 'Proportion of tests for other high contact groups',
      //   type: INPUT_TYPES.number,
      //   min: 0,
      //   max: 1,
      //   step: 0.01,
      //   validation: {
      //     type: 'equals',
      //     value: 1,
      //     keysToMatch: [
      //       'hospitalTestProportion',
      //       'otherHighContactPopulationTestProportion',
      //       'restOfPopulationTestProportion',
      //     ],
      //   },
      //   key: 'otherHighContactPopulationTestProportion',
      // },
      // {
      //   label: 'Proportion of tests for rest of population',
      //   type: INPUT_TYPES.number,
      //   min: 0,
      //   max: 1,
      //   step: 0.01,
      //   validation: {
      //     type: 'equals',
      //     value: 1,
      //     keysToMatch: [
      //       'hospitalTestProportion',
      //       'otherHighContactPopulationTestProportion',
      //       'restOfPopulationTestProportion',
      //     ],
      //   },
      //   key: 'restOfPopulationTestProportion',
      // },
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
            label: 'None',
            value: null,
          },
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
