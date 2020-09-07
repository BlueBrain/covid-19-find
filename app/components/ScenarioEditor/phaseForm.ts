export enum INPUT_TYPES {
  number = 'number',
  select = 'select',
  boolean = 'boolean',
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
        label: 'Trigger',
        type: 'condition',
        key: 'importedInfectionsPerDay',
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
        step: 0.05,
        key: 'sensitivity',
      },
      {
        label: 'Specificity',
        type: INPUT_TYPES.number,
        min: 0,
        max: 1,
        step: 0.05,
        key: 'specificity',
      },
      {
        label: 'Symptomatic only',
        type: INPUT_TYPES.boolean,
        key: 'testSymptomaticOnly',
      },
      {
        label: 'Confirmatory test for positive cases',
        type: INPUT_TYPES.boolean,
        key: 'confirmationTests',
      },
      {
        label: 'Proportion of tests for Health care staff',
        type: INPUT_TYPES.number,
        min: 0,
        max: 1,
        step: 0.05,
        validation: {
          type: 'equals',
          value: 1,
          keysToMatch: [
            'hospitalTestProportion',
            'otherHighContactPopulationTestProportion',
            'restOfPopulationTestProportion',
          ],
        },
        key: 'hospitalTestProportion',
      },
      {
        label: 'Proportion of tests for other high contact groups',
        type: INPUT_TYPES.number,
        min: 0,
        max: 1,
        step: 0.05,
        validation: {
          type: 'equals',
          value: 1,
          keysToMatch: [
            'hospitalTestProportion',
            'otherHighContactPopulationTestProportion',
            'restOfPopulationTestProportion',
          ],
        },
        key: 'otherHighContactPopulationTestProportion',
      },
      {
        label: 'Proportion of tests for rest of population',
        type: INPUT_TYPES.number,
        min: 0,
        max: 1,
        step: 0.05,
        validation: {
          type: 'equals',
          value: 1,
          keysToMatch: [
            'hospitalTestProportion',
            'otherHighContactPopulationTestProportion',
            'restOfPopulationTestProportion',
          ],
        },
        key: 'restOfPopulationTestProportion',
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
