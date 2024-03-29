import * as React from 'react';
import { InputProp } from './phaseForm';

import './phase-input.less';

const PhaseTextInput: React.FC<{
  inputProps: InputProp;
  onChange: (value: string) => void;
  value: string;
}> = ({ inputProps, onChange, value: defaultValue }) => {
  const ref = React.useRef<HTMLInputElement>(null);
  const [inputValue, setInputValue] = React.useState(defaultValue);

  React.useEffect(() => {
    setInputValue(defaultValue?.toString());
  }, [defaultValue]);

  const handleBlur = () => {
    onChange(inputValue);
  };
  const handleChange = () => {
    setInputValue(ref?.current.value);
  };
  return (
    <input
      className="phase text"
      name={inputProps.name || inputProps.key}
      data-key={inputProps.key}
      type="text"
      value={inputValue}
      required
      ref={ref}
      onBlur={handleBlur}
      onChange={handleChange}
      disabled={inputProps.disabled}
    />
  );
};

export default PhaseTextInput;
