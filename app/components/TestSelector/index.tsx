import * as React from 'react';

import useFormInput from '../../hooks/useFormInput';

import './test-selector.less';

export type TestSelectorVales = {
  sensitivityPCR?: number;
  sensitivityRDT?: number;
  sensitivityXray?: number;
  specificityPCR?: number;
  specificityRDT?: number;
  specificityXray?: number;
  numTestsPCR?: number;
  numTestsRDT?: number;
  numTestsXray?: number;
};

const TestSelector: React.FC<TestSelectorVales & {
  onSubmit?: (values: TestSelectorVales) => void;
}> = ({
  sensitivityPCR,
  sensitivityRDT,
  sensitivityXray,
  specificityPCR,
  specificityRDT,
  specificityXray,
  numTestsPCR,
  numTestsRDT,
  numTestsXray,
  onSubmit,
}) => {
  const sensitivityPCRInput = useFormInput(sensitivityPCR, null, true);
  const sensitivityRDTInput = useFormInput(sensitivityRDT, null, true);
  const sensitivityXrayInput = useFormInput(sensitivityXray, null, true);
  const specificityPCRInput = useFormInput(specificityPCR, null, true);
  const specificityRDTInput = useFormInput(specificityRDT, null, true);
  const specificityXrayInput = useFormInput(specificityXray, null, true);
  const numTestsPCRInput = useFormInput(numTestsPCR, null, true);
  const numTestsRDTInput = useFormInput(numTestsRDT, null, true);
  const numTestsXrayInput = useFormInput(numTestsXray, null, true);

  const handleSubmit = e => {
    e.preventDefault();
    onSubmit &&
      onSubmit({
        sensitivityPCR: sensitivityPCRInput.value,
        sensitivityRDT: sensitivityRDTInput.value,
        sensitivityXray: sensitivityXrayInput.value,
        specificityPCR: specificityPCRInput.value,
        specificityRDT: specificityRDTInput.value,
        specificityXray: specificityXrayInput.value,
        numTestsPCR: numTestsPCRInput.value,
        numTestsRDT: numTestsRDTInput.value,
        numTestsXray: numTestsXrayInput.value,
      });
    if (e.target.checkValidity()) {
      document.querySelector('#simulation-results')?.scrollIntoView({
        behavior: 'smooth',
      });
    }
  };

  return (
    <form className="tests-form" onSubmit={handleSubmit} id="tests-form">
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
                    {...numTestsPCRInput}
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
                    {...sensitivityPCRInput}
                    step="0.01"
                    min="0"
                    max="1"
                    required
                  />
                  <label className="label-mini">Specificity</label>
                  <input
                    {...specificityPCRInput}
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
                    {...numTestsRDTInput}
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
                    {...sensitivityRDTInput}
                    step="0.01"
                    min="0"
                    max="1"
                    required
                  />
                  <label className="label-mini">Specificity</label>
                  <input
                    {...specificityRDTInput}
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
                    {...numTestsXrayInput}
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
                    {...sensitivityXrayInput}
                    step="0.01"
                    min="0"
                    max="1"
                    required
                  />
                  <label className="label-mini">Specificity</label>
                  <input
                    {...specificityXrayInput}
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
