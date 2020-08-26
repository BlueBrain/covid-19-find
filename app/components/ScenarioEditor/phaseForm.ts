export enum INPUT_TYPES {
  number = 'number',
  select = 'select',
}

export type InputProp = {
  label: string;
  type: INPUT_TYPES;
  prop: string;
  disabled?: boolean;
  required?: boolean;
};

export type NumberInputProp = InputProp & {
  type: INPUT_TYPES.number;
  min?: number;
  max?: number;
  step?: number;
};

export type SelectInputProp = {
  type: INPUT_TYPES.select;
  options: {
    value: string | null;
    label: string;
  }[];
};

export default [
  {
    title: 'Epidemic',
    input: [
      {
        label: 'Imported infections per day',
        type: INPUT_TYPES.number,
        min: 0,
        prop: 'imported_infections_per_day',
      },
    ],
  },
  {
    title: 'Government Intervention',
    input: [
      {
        label: 'Trigger',
        type: 'condition',
        prop: 'imported_infections_per_day',
      },
      {
        label: 'Severity',
        type: INPUT_TYPES.number,
        min: 0,
        max: 1,
        step: 0.1,
        prop: 'severirt',
      },
    ],
  },
  {
    title: 'Contact Tracing',
    input: [
      {
        label: 'Trace and isolate contacts',
        type: INPUT_TYPES.select,
        prop: 'prop_contacts_traced',
        options: [
          {
            label: 'None',
            value: null,
          },
          {
            label: '10%',
            value: '10%',
          },
          {
            label: '25%',
            value: '25%',
          },
          {
            label: '50%',
            value: '50%',
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
        prop: 'num_tests_mitigation',
      },
      {
        label: 'Test Type',
        type: INPUT_TYPES.select,
        min: 0,
        prop: 'Type_test_mitigation',
        options: [
          {
            label: 'None',
            value: null,
          },
        ],
      },
    ],
  },
];
