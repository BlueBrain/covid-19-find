import * as React from 'react';
import { NumberInputProp } from './phaseForm';

import './phase-input.less';

const PhaseNumberInput: React.FC<{
  inputProps: NumberInputProp;
  onChange: (number) => void;
  value: number;
}> = ({ inputProps, onChange, value }) => {
  const ref = React.useRef<HTMLInputElement>(null);
  const [inputValue, setInputValue] = React.useState(value.toString());
  React.useEffect(() => {
    setInputValue(value.toString());
  }, [value]);
  const handleBlur = () => {
    onChange(inputValue);
  };
  const handleChange = () => {
    setInputValue(ref?.current.value);
  };
  return (
    <input
      className="phase number"
      name={inputProps.name || inputProps.key}
      data-key={inputProps.key}
      min={inputProps.min}
      max={inputProps.max}
      step={inputProps.step}
      defaultValue={value}
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
