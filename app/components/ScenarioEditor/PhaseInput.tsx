import * as React from 'react';
import { NumberInputProp, SelectInputProp, INPUT_TYPES } from './phaseForm';
import PhaseNumberInput from './PhaseNumberInput';

const PhaseInput: React.FC<{
  inputProps: NumberInputProp | SelectInputProp;
  onChange: (value: string | number | boolean | null) => void;
}> = ({ inputProps, onChange }) => {
  if (inputProps.type === INPUT_TYPES.select) {
    return <input />;
  }
  if (inputProps.type === INPUT_TYPES.number) {
    return <PhaseNumberInput inputProps={inputProps} onChange={onChange} />;
  }
  return null;
};

export default PhaseInput;
