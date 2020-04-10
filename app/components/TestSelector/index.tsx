import * as React from 'react';

import useFormInput from '../../hooks/useFormInput';

import './test-selector.less';

export type TestSelectorVales = {
  sensitivity_PCR?: number;
  sensitivity_RDT?: number;
  sensitivity_xray?: number;
  selectivity_PCR?: number;
  selectivity_RDT?: number;
  selectivity_xray?: number;
  num_tests_PCR?: number;
  num_tests_RDT?: number;
  num_tests_xray?: number;
};

const TestSelector: React.FC<TestSelectorVales & {
  onSubmit?: (values: TestSelectorVales) => void;
}> = ({
  sensitivity_PCR,
  sensitivity_RDT,
  sensitivity_xray,
  selectivity_PCR,
  selectivity_RDT,
  selectivity_xray,
  num_tests_PCR,
  num_tests_RDT,
  num_tests_xray,
  onSubmit,
}) => {
  const formRef = React.useRef<HTMLFormElement>(null);
  const PCRsSensitivity = useFormInput(sensitivity_PCR);
  const PCRtotal = useFormInput(num_tests_PCR);
  const rapidTestKitTotal = useFormInput(num_tests_RDT);
  const chestXRayTotal = useFormInput(num_tests_xray);
  const rapidTestKitsSensitivity = useFormInput(sensitivity_RDT);
  const xRaysSensitivity = useFormInput(sensitivity_xray);
  const PCRsSelectivity = useFormInput(selectivity_PCR);
  const rapidTestKitsSelectivity = useFormInput(selectivity_RDT);
  const xRaysSelectivity = useFormInput(selectivity_xray);

  const handleSubmit = e => {
    e.preventDefault();
    onSubmit &&
      onSubmit({
        sensitivity_PCR: PCRsSensitivity.value,
        sensitivity_RDT: rapidTestKitsSensitivity.value,
        sensitivity_xray: xRaysSensitivity.value,
        selectivity_PCR: PCRsSelectivity.value,
        selectivity_RDT: rapidTestKitsSelectivity.value,
        selectivity_xray: xRaysSelectivity.value,
        num_tests_PCR: PCRtotal.value,
        num_tests_RDT: rapidTestKitTotal.value,
        num_tests_xray: chestXRayTotal.value,
      });
  };

  return (
    <form className="tests-form" ref={formRef} onSubmit={handleSubmit}>
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
            <div className="tests-form-container">
              <div className="input test-box">
                <p className="test-description">
                  Maximal deployment
                  <br />
                  <em>PCRs*</em>
                  <br />
                  per day
                  <input
                    {...PCRtotal}
                    placeholder={'Enter... [0-100]'}
                    style={{
                      width: '200px',
                      margin: '1rem auto',
                    }}
                    required
                  />
                </p>
                <div className="test-input">
                  <label className="label-mini">Sensitivity</label>
                  <input
                    {...PCRsSensitivity}
                    step="0.01"
                    min="0"
                    max="1"
                    required
                  />
                  <label className="label-mini">Specificity</label>
                  <input
                    {...PCRsSelectivity}
                    step="0.01"
                    min="0"
                    max="1"
                    required
                  />
                </div>
              </div>
              <div className="input test-box">
                <p className="test-description">
                  Maximal deployment of
                  <br />
                  <em>Rapid Test Kits</em>
                  <br />
                  per day
                  <input
                    {...rapidTestKitTotal}
                    placeholder={'Enter... [0-100]'}
                    style={{
                      width: '200px',
                      margin: '1rem auto',
                    }}
                    required
                  />
                </p>
                <div className="test-input">
                  <label className="label-mini">Sensitivity</label>
                  <input
                    {...rapidTestKitsSensitivity}
                    step="0.01"
                    min="0"
                    max="1"
                    required
                  />
                  <label className="label-mini">Specificity</label>
                  <input
                    {...rapidTestKitsSelectivity}
                    step="0.01"
                    min="0"
                    max="1"
                    required
                  />
                </div>
              </div>
              <div className="input test-box">
                <p className="test-description">
                  Maximal deployment of
                  <br />
                  <em>Chest X-rays</em>
                  <br />
                  per day
                  <input
                    {...chestXRayTotal}
                    placeholder={'Enter... [0-100]'}
                    style={{
                      width: '200px',
                      margin: '1rem auto',
                    }}
                    required
                  ></input>
                </p>
                <div className="test-input">
                  <label className="label-mini">Sensitivity</label>
                  <input
                    {...xRaysSensitivity}
                    step="0.01"
                    min="0"
                    max="1"
                    required
                  />
                  <label className="label-mini">Specificity</label>
                  <input
                    {...xRaysSelectivity}
                    step="0.01"
                    min="0"
                    max="1"
                    required
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="submit-button">
            <button className="action submit-button" type="submit">
              Submit
            </button>
          </div>
        </div>
        <div className="triangle"></div>
      </section>
    </form>
  );
};

export default TestSelector;
