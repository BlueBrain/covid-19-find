import * as React from 'react';
import { match } from 'ts-pattern';
import {
  NumberInputProp,
  SelectInputProp,
  INPUT_TYPES,
  BooleanInputProp,
  InputProp,
} from './phaseForm';
import PhaseNumberInput from './PhaseNumberInput';
import PhaseSelectInput from './PhaseSelectInput';
import PhaseSwitchInput from './PhaseSwitch';
import PhaseTextInput from './PhaseTextInput';

export type PhaseInputProps = {
  inputProps: NumberInputProp | SelectInputProp | BooleanInputProp | InputProp;
  onChange: (value: string | number | boolean | null) => void;
  value?: string | number | boolean | null;
};

const PhaseInput: React.FC<PhaseInputProps> = ({
  inputProps,
  onChange,
  value,
}) => {
  return match(inputProps.type)
    .with(INPUT_TYPES.number, () => (
      <PhaseNumberInput
        {...{
          inputProps: inputProps as NumberInputProp,
          onChange,
          value: value as number,
        }}
      />
    ))
    .with(INPUT_TYPES.select, () => (
      <PhaseSelectInput
        {...{
          inputProps: inputProps as SelectInputProp,
          onChange,
          value: value as string,
        }}
      />
    ))
    .with(INPUT_TYPES.boolean, () => (
      <PhaseSwitchInput
        {...{
          inputProps: inputProps as BooleanInputProp,
          onChange,
          value: value as boolean,
        }}
      />
    ))

    .with(INPUT_TYPES.text, () => (
      <PhaseTextInput
        {...{
          inputProps,
          onChange,
          value: value as string,
        }}
      />
    ))
    .run();
};

export default PhaseInput;
