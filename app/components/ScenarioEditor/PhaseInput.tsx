import * as React from 'react';
import {
  NumberInputProp,
  SelectInputProp,
  INPUT_TYPES,
  BooleanInputProp,
} from './phaseForm';
import PhaseNumberInput from './PhaseNumberInput';
import PhaseSelectInput from './PhaseSelectInput';
import PhaseSwitchInput from './PhaseSwitch';

export type PhaseInputProps = {
  inputProps: NumberInputProp | SelectInputProp | BooleanInputProp;
  onChange: (value: string | number | boolean | null) => void;
  value?: string | number | boolean | null;
};

const PhaseInput: React.FC<PhaseInputProps> = ({
  inputProps,
  onChange,
  value,
}) => {
  let inputComponent: React.FC<PhaseInputProps> = PhaseNumberInput;
  if (inputProps.type === INPUT_TYPES.select) {
    inputComponent = PhaseSelectInput;
  } else if (inputProps.type === INPUT_TYPES.boolean) {
    inputComponent = PhaseSwitchInput;
  }
  return inputComponent({
    inputProps,
    onChange,
    value,
  });
};

export default PhaseInput;
