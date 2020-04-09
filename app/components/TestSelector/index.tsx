import * as React from 'react';

import useFormInput from '../../hooks/useFormInput';

import './test-selector.less';

const TestSelector: React.FC = () => {
  const PCRsSensitivity = useFormInput('');
  const rapidTestKitsSensitivity = useFormInput('');
  const xRaysSensitivity = useFormInput('');
  const PCRsSelectivity = useFormInput('');
  const rapidTestKitsSelectivity = useFormInput('');
  const xRaysSelectivity = useFormInput('');

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
                <p className="test-description">
                  Maximal deployment
                  <br />
                  <em>PCRs*</em>
                  <br />
                  per day
                </p>
                <div className="test-input">
                  <label className="label-mini">Sensitivity</label>
                  <input {...PCRsSensitivity} />
                  <label className="label-mini">Selectivity</label>
                  <input {...PCRsSelectivity} />
                </div>
              </div>
              <div className="input test-box">
                <p className="test-description">
                  Maximal deployment of
                  <br />
                  <em>Rapid Test Kits</em>
                  <br />
                  per day
                </p>
                <div className="test-input">
                  <label className="label-mini">Sensitivity</label>
                  <input {...rapidTestKitsSensitivity} />
                  <label className="label-mini">Selectivity</label>
                  <input {...rapidTestKitsSelectivity} />
                </div>
              </div>
              <div className="input test-box">
                <p className="test-description">
                  Maximal deployment of
                  <br />
                  <em>Chest X-rays</em>
                  <br />
                  per day
                </p>
                <div className="test-input">
                  <label className="label-mini">Sensitivity</label>
                  <input {...xRaysSensitivity} />
                  <label className="label-mini">Selectivity</label>
                  <input {...xRaysSelectivity} />
                </div>
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
