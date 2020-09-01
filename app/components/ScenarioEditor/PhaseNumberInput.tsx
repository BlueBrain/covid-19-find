import * as React from 'react';
import { NumberInputProp } from './phaseForm';

const PhaseNumberInput: React.FC<{
  inputProps: NumberInputProp;
  onChange: (number) => void;
  value: number;
}> = ({ inputProps, onChange, value }) => {
  const ref = React.useRef<HTMLInputElement>(null);
  const [inputValue, setInputValue] = React.useState(value);
  const handleBlur = () => {
    onChange(inputValue);
  };
  const handleChange = () => {
    setInputValue(Number(ref?.current.value));
  };
  return (
    <input
      min={inputProps.min}
      max={inputProps.max}
      step={inputProps.step}
      value={inputValue}
      type="number"
      required
      ref={ref}
      onBlur={handleBlur}
      onChange={handleChange}
      disabled={inputProps.disabled}
    />
  );
};

export default PhaseNumberInput;
