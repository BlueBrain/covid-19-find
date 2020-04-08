import * as React from 'react';

const useFormInput = initialValue => {
  const [value, setValue] = React.useState(initialValue);

  const onHandleChange = e => {
    setValue(e.target.value);
  };

  return {
    value,
    onChange: onHandleChange,
    placeholder: 'Enter... [1-100]',
  };
};

export default useFormInput;
