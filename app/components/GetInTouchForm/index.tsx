import * as React from 'react';

import useFormInput from '../../hooks/useFormInput';

import './get-in-touch-form.less';

export type GetIntTouchInput = {
  name: string;
  email: string;
  subject: string;
  query: string;
};

export type GetInTouchFormProps = {
  onSubmit: (values: GetIntTouchInput) => void;
};

const getInTouchForm: React.FC<GetInTouchFormProps> = ({ onSubmit }) => {
  const [disabled, setDisabled] = React.useState(false);
  const [showSuccessMessage, setshowSuccessMessage] = React.useState(false);
  const name = useFormInput('');
  const email = useFormInput('');
  const subject = useFormInput('');
  const query = useFormInput('');

  const onClickSubmit = event => {
    event.preventDefault();

    setDisabled(true);
    setshowSuccessMessage(true);

    onSubmit({
      name: name.value,
      email: email.value,
      subject: subject.value,
      query: subject.value,
    });
  };

  return (
    <>
      <em>Get in touch</em>
      <form className="get-in-touch-form">
        <input {...name} placeholder="Name" disabled={disabled} />
        <input
          {...email}
          placeholder="E-mail"
          disabled={disabled}
          type="email"
        />
        <input {...subject} placeholder="Subject" disabled={disabled} />
        <textarea
          {...query}
          placeholder="Query"
          className="query"
          disabled={disabled}
          required
        />
        {showSuccessMessage ? (
          <p>Thank you! You message was submitted succesfully.</p>
        ) : (
          <button type="submit" onClick={onClickSubmit} disabled={disabled}>
            Enter
          </button>
        )}
      </form>
    </>
  );
};

export default getInTouchForm;
