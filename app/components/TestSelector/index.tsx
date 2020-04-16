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
                  <a data-tip data-for="pcr-tooltip">
                    <em>
                      PCRs <IoIosInformationCircleOutline />
                    </em>
                  </a>
                  <ReactTooltip id="pcr-tooltip">
                    <p>
                      These test kits use the Polymerase Chain Reaction (PCR) to
                      amplify fragments of viral DNA present in patient samples.
                      PCR-based test kits have high sensitivity (they catch
                      nearly all cases) and high specificity (they produce
                      relatively few false positives). For this reason, they are
                      the gold standard for COVID-19 testing. However, samples
                      need to be tested in the laboratory. Testing requires good
                      logistics (to bring samples to the lab), skilled staff,
                      and expensive equipment. Even in ideal conditions response
                      times may be relatively slow.
                    </p>
                  </ReactTooltip>
                  <br />
                  per day
                  <input
                    {...numTestsPCRInput}
                    style={{
                      width: '200px',
                      margin: '1rem auto',
                    }}
                    min="0"
                    type="number"
                    required
                  />
                </p>
                <div className="test-input">
                  <a data-tip data-for="sensitivity-tooltip">
                    <label className="label-mini">
                      Sensitivity <IoIosInformationCircleOutline />
                    </label>
                  </a>
                  <ReactTooltip id="sensitivity-tooltip">
                    <p>
                      The sensitivity of a diagnostic test represents the
                      proportion of infections the test is capable of detecting.
                      A test with a sensitivity of 1.0 will detect all
                      infections present in a patient group. A test with a
                      sensitivity of 0.85 will detect just 85% of infections.
                      The remaining 15% (“false negatives”) will continue to
                      spread the infection in the community. For this reason, it
                      is important that a test designed to identify and isolate
                      infected people should have a high sensitivity.
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
                  <a data-tip data-for="specificity-tooltip">
                    <label className="label-mini">
                      Specificity <IoIosInformationCircleOutline />
                    </label>
                  </a>
                  <ReactTooltip id="specificity-tooltip">
                    <p>
                      The specificity of a diagnostic test represents the
                      percentage of healthy people who are correctly identified
                      as not having the condition being tested for. A test with
                      a specificity of 1.0 will never give a positive result for
                      a person who does not have the infection. A test with a
                      specificity of 0.85 will give correct results for just 85%
                      of healthy people. The remaining 15% will be false
                      positives. False positive results have a negative impact
                      on the individuals concerned (anxiety, social isolation,
                      loss of work), and places a heavy burden on the health
                      service that has to treat them as if they were sick. For
                      this reason it is important that tests should have high
                      specificity.
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
              <div className="input test-box">
                <p className="test-description">
                  Maximal deployment of
                  <br />
                  <a data-tip data-for="rdt-tooltip">
                    <em>
                      Rapid Test Kits <IoIosInformationCircleOutline />
                    </em>
                  </a>
                  <ReactTooltip id="rdt-tooltip">
                    <p>
                      These test kits test for the presence of viral antigens or
                      antibodies. They do not require a lab and give a fast
                      response. However, they are unable to detect early stage
                      infections (when antibodies have yet to form) and may also
                      give false positive results . Furthermore many test kits
                      on the market have not yet been tested independently. RDTs
                      may be useful for monitoring the presence of COVID-19 in
                      the population or for identifying individuals who have
                      acquired immunity to the virus. They are not considered as
                      a reliable tool to identify and isolate infected people.
                    </p>
                  </ReactTooltip>
                  <br />
                  per day
                  <input
                    {...numTestsRDTInput}
                    style={{
                      width: '200px',
                      margin: '1rem auto',
                    }}
                    min="0"
                    type="number"
                    required
                  />
                </p>
                <div className="test-input">
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
              <div className="input test-box">
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
                    style={{
                      width: '200px',
                      margin: '1rem auto',
                    }}
                    min="0"
                    type="number"
                    required
                  ></input>
                </p>
                <div className="test-input">
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
