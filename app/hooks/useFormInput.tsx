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
    value: value || '',
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

export const useCheckbox = (
  initialValue: any,
  placeholder?: any,
  override?: boolean,
) => {
  const [value, setValue] = React.useState(initialValue);

  const onHandleChange = e => {
    setValue(e ? e.target.checked : value);
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
