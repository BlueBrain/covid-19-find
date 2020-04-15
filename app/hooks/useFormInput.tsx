import * as React from 'react';

const useFormInput = (
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

export default useFormInput;
