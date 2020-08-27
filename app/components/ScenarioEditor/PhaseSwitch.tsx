import * as React from 'react';
import { BooleanInputProp } from './phaseForm';
import Switch from 'react-switch';
import colors from '../../colors';

const PhaseSwitchInput: React.FC<{
  inputProps: BooleanInputProp;
  onChange: (number) => void;
  value: boolean;
}> = ({ inputProps, onChange, value }) => {
  return (
    <div style={{ textAlign: 'left', marginTop: '5px' }}>
      <Switch
        onChange={onChange}
        checked={value}
        onColor={colors.turqouise}
        offColor={'#c3c9cc'}
        disabled={inputProps.disabled}
      />
    </div>
  );
};

export default PhaseSwitchInput;
