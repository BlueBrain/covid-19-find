import * as React from 'react';

export const useFormInput = (
  initialValue: any,
  placeholder?: any,
  override?: boolean,
) => {
  const [value, setValue] = React.useState(initialValue);

  const onHandleChange = e => {
    setValue(e ? e.target.value : value);
  };

  React.useEffect(() => {
    if (override) {
      setValue(initialValue);
    }
  }, [initialValue, override]);

  return {
    // NOTE: empty or null input must be an empty string for html5
    // This checks to make sure the value is not 0 before
    // marking the value as empty
    value: value || (value === 0 ? 0 : ''),
    onChange: onHandleChange,
    placeholder: placeholder || 'Enter... ',
  };
};

export const useTextInput = (
  initialValue: any,
  placeholder?: any,
  override?: boolean,
) => {
  const [value, setValue] = React.useState(initialValue);

  const onHandleChange = e => {
    setValue(e ? e.target.value : value);
  };

  React.useEffect(() => {
    if (override) {
      setValue(initialValue);
    }
  }, [initialValue, override]);

  return {
    value: value || '',
    onChange: onHandleChange,
    placeholder: placeholder || 'Enter... ',
  };
};

export const useDirectInput = (
  initialValue: any,
  placeholder?: any,
  override?: boolean,
) => {
  const [value, setValue] = React.useState(initialValue);

  const onHandleChange = newValue => {
    setValue(newValue);
  };

  React.useEffect(() => {
    if (override) {
      setValue(initialValue);
    }
  }, [initialValue, override]);

  return {
    value,
    onChange: onHandleChange,
    placeholder: placeholder || 'Enter... ',
  };
};

export const useSelectInput = (
  initialValue: any,
  placeholder?: any,
  override?: boolean,
) => {
  const [value, setValue] = React.useState(initialValue);

  const onHandleChange = ({ value: newValue }) => {
    setValue(newValue);
  };

  React.useEffect(() => {
    if (override) {
      setValue(initialValue);
    }
  }, [initialValue, override]);

  return {
    value: value || '',
    onChange: onHandleChange,
    placeholder: placeholder || 'Enter... ',
  };
};

export default useFormInput;
