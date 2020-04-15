import * as React from 'react';

import useFormInput from '../../hooks/useFormInput';

const getInTouchForm: React.FC = () => {
  const [buttonName, setButtonName] = React.useState('Submit');
  const [disabled, setDisabled] = React.useState(false);
  const name = useFormInput('');
  const email = useFormInput('');
  const subject = useFormInput('');
  const query = useFormInput('');

  const onClickSubmit = event => {
    event.preventDefault();
    setDisabled(true);
    console.log(name, email, subject, query);
    setButtonName('Thank You!');
  };

  return (
    <>
      <em>Get in touch</em>
      <form>
        <input {...name} placeholder="Name" />
        <input {...email} placeholder="E-mail" />
        <input {...subject} placeholder="Subject" />
        <textarea {...query} placeholder="Query" className="query" />
        <button type="submit" onClick={onClickSubmit} disabled={disabled}>
          {buttonName}
        </button>
      </form>
    </>
  );
};

export default getInTouchForm;
