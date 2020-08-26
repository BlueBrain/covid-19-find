import * as React from 'react';
import { NumberInputProp } from './phaseForm';

const PhaseNumberInput: React.FC<{
  inputProps: NumberInputProp;
  onChange: (number) => void;
}> = ({ inputProps, onChange }) => {
  const ref = React.useRef<HTMLInputElement>(null);
  const handleBlur = () => {
    onChange(ref.current.value);
  };
  return (
    <input
      min={inputProps.min}
      max={inputProps.max}
      step={inputProps.step}
      type="number"
      required
      ref={ref}
      onBlur={handleBlur}
      disabled={inputProps.disabled}
    />
  );
};

export default PhaseNumberInput;
