import * as React from 'react';
import { NumberInputProp } from './phaseForm';

import './phase-input.less';

const PhaseNumberInput: React.FC<{
  inputProps: NumberInputProp;
  onChange: (value: number | string) => void;
  value: number;
}> = ({ inputProps, onChange, value: defaultValue }) => {
  const ref = React.useRef<HTMLInputElement>(null);
  const [inputValue, setInputValue] = React.useState<string>(
    defaultValue?.toString(),
  );

  React.useEffect(() => {
    setInputValue(defaultValue?.toString());
  }, [defaultValue]);

  const handleBlur = () => {
    onChange(!isNaN(Number(inputValue)) ? Number(inputValue) : inputValue);
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
