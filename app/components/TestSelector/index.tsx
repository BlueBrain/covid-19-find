import * as React from 'react';

import useFormInput from '../../hooks/useFormInput';

import './test-selector.less';
import ReactTooltip from 'react-tooltip';
import { IoIosInformationCircleOutline } from 'react-icons/io';

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
  children,
}) => {
  const sensitivityPCRInput = useFormInput(sensitivityPCR, null, true);
  const sensitivityRDTInput = useFormInput(sensitivityRDT, null, true);
  // const sensitivityXrayInput = useFormInput(sensitivityXray, null, true);
  const specificityPCRInput = useFormInput(specificityPCR, null, true);
  const specificityRDTInput = useFormInput(specificityRDT, null, true);
  // const specificityXrayInput = useFormInput(specificityXray, null, true);
  const numTestsPCRInput = useFormInput(numTestsPCR, null, true);
  const numTestsRDTInput = useFormInput(numTestsRDT, null, true);
  // const numTestsXrayInput = useFormInput(numTestsXray, null, true);

  const handleSubmit = e => {
    e.preventDefault();
    e.target.dataset.dirty = true;
    onSubmit &&
      onSubmit({
        sensitivityPCR: sensitivityPCRInput.value,
        sensitivityRDT: sensitivityRDTInput.value,
        // sensitivityXray: sensitivityXrayInput.value,
        specificityPCR: specificityPCRInput.value,
        specificityRDT: specificityRDTInput.value,
        // specificityXray: specificityXrayInput.value,
        numTestsPCR: numTestsPCRInput.value,
        numTestsRDT: numTestsRDTInput.value,
        // numTestsXray: numTestsXrayInput.value,
      });
  };

  return (
    <form className="tests-form" id="tests-form" onSubmit={handleSubmit}>
      <section>
        <div className="test-selector action-box">
          <div className="title">
            <div className="number">
              <span>2</span>
            </div>
            <h2 className="underline">
              Enter your <em>test availabilities</em>
            </h2>
          </div>
          <div className="container">
            <div className="tests-form-container">
              <div className="input test-box">
                <div className="test-description">
                  Maximum number of
                  <br />
                  <a data-tip data-for="pcr-tooltip">
                    <em>
                      molecular (PCR) tests <IoIosInformationCircleOutline />
                    </em>
                  </a>
                  <br />
                  That can be performed per day
                  <ReactTooltip id="pcr-tooltip">
                    <p>
                      Molecular tests, also known as polymerase chain reaction
                      (PCR) tests, amplify fragments of viral DNA so they can be
                      detected in patient samples. PCR-based tests have high
                      sensitivity (they correctly identify nearly all cases) and
                      high specificity (they rarely incorrectly indicate a
                      negative case as positive). However, PCR testing needs to
                      be done in a laboratory, with supporting infrastructure
                      and skilled technicians.
                    </p>
                  </ReactTooltip>
                  <br />
                  per day
                  <input {...numTestsPCRInput} min="0" type="number" required />
                </div>
                <div className="test-input">
                  <div>
                    <a data-tip data-for="sensitivity-tooltip">
                      <label className="label-mini">
                        Sensitivity <IoIosInformationCircleOutline />
                      </label>
                    </a>
                    <ReactTooltip id="sensitivity-tooltip">
                      <p>
                        The sensitivity of a diagnostic test represents the
                        proportion of infections the test is capable of
                        detecting. A test with a sensitivity of 1.0 will detect
                        all infections present in a patient group. A test with a
                        sensitivity of 0.85 will detect just 85% of infections.
                        The remaining 15% (“false negatives”) will continue to
                        spread the infection in the community. For this reason,
                        it is important that a test designed to identify and
                        isolate infected people should have a high sensitivity.
                      </p>
                    </ReactTooltip>
                    <input
                      {...sensitivityPCRInput}
                      step="0.01"
                      min="0"
                      max="1"
                      type="number"
                      required
                    />
                  </div>
                  <div>
                    <a data-tip data-for="specificity-tooltip">
                      <label className="label-mini">
                        Specificity <IoIosInformationCircleOutline />
                      </label>
                    </a>
                    <ReactTooltip id="specificity-tooltip">
                      <p>
                        The specificity of a diagnostic test represents the
                        percentage of healthy people who are correctly
                        identified as not having the condition being tested for.
                        A test with a specificity of 1.0 will never give a
                        positive result for a person who does not have the
                        infection. A test with a specificity of 0.85 will give
                        correct results for just 85% of healthy people. The
                        remaining 15% will be false positives. False positive
                        results have a negative impact on the individuals
                        concerned (anxiety, social isolation, loss of work), and
                        places a heavy burden on the health service that has to
                        treat them as if they were sick. For this reason it is
                        important that tests should have high specificity.
                      </p>
                    </ReactTooltip>
                    <input
                      {...specificityPCRInput}
                      step="0.01"
                      min="0"
                      max="1"
                      type="number"
                      required
                    />
                  </div>
                </div>
              </div>
              <div className="input test-box">
                <p className="test-description">
                  Maximum number of
                  <br />
                  <a data-tip data-for="rdt-tooltip">
                    <em>
                      Rapid Diagnostic Tests <IoIosInformationCircleOutline />
                    </em>
                  </a>
                  <br />
                  that can be performed per day
                  <ReactTooltip id="rdt-tooltip">
                    <p>
                      Rapid diagnostic tests (RDTs) identify the presence of
                      viral antigens (to determine active infection) or
                      antibodies (to indicate previous infection) in a patient
                      sample. Similar to pregnancy tests, they do not require a
                      laboratory and can give a fast response. However they are
                      not yet as accurate as molecular tests, and are not yet
                      considered to be reliable enough for patient management
                    </p>
                  </ReactTooltip>
                  <br />
                  per day
                  <input {...numTestsRDTInput} min="0" type="number" required />
                </p>
                <div className="test-input">
                  <div>
                    <a data-tip data-for="sensitivity-tooltip">
                      <label className="label-mini">
                        Sensitivity <IoIosInformationCircleOutline />
                      </label>
                    </a>
                    <input
                      {...sensitivityRDTInput}
                      step="0.01"
                      min="0"
                      max="1"
                      type="number"
                      required
                    />
                  </div>
                  <div>
                    <a data-tip data-for="specificity-tooltip">
                      <label className="label-mini">
                        Specificity <IoIosInformationCircleOutline />
                      </label>
                    </a>
                    <input
                      {...specificityRDTInput}
                      step="0.01"
                      min="0"
                      max="1"
                      type="number"
                      required
                    />
                  </div>
                </div>
              </div>
              {/* <div className="input test-box">
                <p className="test-description">
                  Maximal deployment of
                  <br />
                  <a data-tip data-for="xray-tooltip">
                    <em>
                      Chest X-rays <IoIosInformationCircleOutline />
                    </em>
                  </a>
                  <ReactTooltip id="xray-tooltip">
                    <p>
                      Severe cases of COVID-19 affect the lungs in ways that are
                      easily visible on a chest x-ray. Chest x-rays are thus a
                      highly effective way of detecting such cases in a hospital
                      setting. They are effective as a way of identifying milder
                      cases of the disease.
                    </p>
                  </ReactTooltip>
                  <br />
                  per day
                  <input
                    {...numTestsXrayInput}
                    min="0"
                    type="number"
                    required
                  ></input>
                </p>
                <div className="test-input">
                  <div>
                    <a data-tip data-for="sensitivity-tooltip">
                      <label className="label-mini">
                        Sensitivity <IoIosInformationCircleOutline />
                      </label>
                    </a>
                    <input
                      {...sensitivityXrayInput}
                      step="0.01"
                      min="0"
                      max="1"
                      type="number"
                      required
                    />
                  </div>
                  <div>
                    <a data-tip data-for="specificity-tooltip">
                      <label className="label-mini">
                        Specificity <IoIosInformationCircleOutline />
                      </label>
                    </a>
                    <input
                      {...specificityXrayInput}
                      step="0.01"
                      min="0"
                      max="1"
                      type="number"
                      required
                    />
                  </div>
                </div>
              </div> */}
            </div>
          </div>
          <div className="submit-button">
            <button className="action submit-button" type="submit">
              Enter
            </button>
          </div>
          <div>{children}</div>
        </div>
        <div className="triangle"></div>
      </section>
    </form>
  );
};

export default TestSelector;
