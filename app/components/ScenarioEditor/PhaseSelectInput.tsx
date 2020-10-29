import * as React from 'react';
import Select from 'react-select';
import Color from 'color';
import { SelectInputProp } from './phaseForm';
import colors from '../../colors';
import { useSelectInput } from '../../hooks/useFormInput';

const PhaseSelectInput: React.FC<{
  inputProps: SelectInputProp;
  onChange: (number) => void;
  value?: string | number | null;
}> = ({ inputProps, onChange, value }) => {
  const select = useSelectInput(null, null, true);

  const handleBlur = () => {
    onChange(select.value);
  };

  return (
    <Select
      isDisabled={inputProps.disabled}
      defaultValue={inputProps.options.find(
        ({ value: optionValue }) => optionValue === value,
      )}
      onChange={select.onChange}
      onBlur={handleBlur}
      options={inputProps.options}
      // @ts-ignore
      theme={theme => ({
        ...theme,
        borderRadius: '10px',
        colors: {
          ...theme.colors,
          primary25: Color(colors.turqouise)
            .alpha(0.25)
            .toString(),
          primary: colors.turqouise,
        },
      })}
      styles={{
        valueContainer: defaults => ({
          ...defaults,
          height: '39px',
        }),
        container: defaults => ({
          ...defaults,
          margin: '5px 0 10px 0',
        }),
      }}
    />
  );
};

export default PhaseSelectInput;
