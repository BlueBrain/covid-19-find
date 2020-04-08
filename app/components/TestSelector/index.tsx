import * as React from 'react';

import useFormInput from '../../hooks/useFormInput';

import './test-selector.less';

const TestSelector: React.FC = () => {
  const PCRs = useFormInput('');
  const rapidTestKits = useFormInput('');
  const xRays = useFormInput('');

  const onClickSubmit = data => {
    console.log('clicked');
  };

  return (
    <section>
      <div className="test-selector action-box">
        <div className="title">
          <div className="number">
            <span>2</span>
          </div>
          <h2 className="underline">
            Select and view <em>test availabilities</em>
          </h2>
        </div>
        <div className="container">
          <form className="tests-form">
            <div className="tests-form-container">
              <div className="input test-box">
                <div>
                  <label>
                    Maximal deployment
                    <br />
                    <em>PCRs</em>
                    <br />
                    (primary care requirements)
                    <br />
                    per day
                  </label>
                </div>
                <div>
                  <input {...PCRs} />
                </div>
              </div>
              <div className="input test-box">
                <label>
                  Maximal deployment of
                  <br />
                  <em>Rapid Test Kits</em>
                  <br />
                  per day
                </label>
                <input {...rapidTestKits} />
              </div>
              <div className="input test-box">
                <label>
                  Maximal deployment of
                  <br />
                  <em>Chest X-rays</em>
                  <br />
                  per day
                </label>
                <input {...xRays} />
              </div>
            </div>
          </form>
        </div>
        <div className="submit-button">
          <button className="action submit-button" onClick={onClickSubmit}>
            Submit
          </button>
        </div>
      </div>
      <div className="triangle"></div>
    </section>
  );
};

export default TestSelector;
