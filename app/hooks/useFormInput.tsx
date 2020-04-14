import * as React from 'react';

const useFormInput = (initialValue: any, placeholder?: any) => {
  const [value, setValue] = React.useState(initialValue);

  const onHandleChange = e => {
    setValue(e ? e.target.value : value);
  };

  const changeValue = (value: any) => {
    setValue(value);
  };

  return {
    value,
    changeValue,
    onChange: onHandleChange,
    placeholder: placeholder || 'Enter... [1-100]',
  };
};

export default useFormInput;
