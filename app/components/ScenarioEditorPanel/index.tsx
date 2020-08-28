import * as React from 'react';

import ScenarioEditor from '../ScenarioEditor/ScenarioList';
import useFormInput from '../../hooks/useFormInput';
import { ClientScenarioData } from '../../types/simulation';

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
  scenarios?: ClientScenarioData[];
};

const TestSelector: React.FC<TestSelectorVales & {
  onSubmit?: (values: TestSelectorVales) => void;
  testsFormReady: boolean;
  setTestsFormReady: (value: boolean) => void;
}> = ({
  scenarios,
  sensitivityPCR,
  sensitivityRDT,
  specificityPCR,
  specificityRDT,
  numTestsPCR,
  numTestsRDT,
  onSubmit,
  testsFormReady,
  setTestsFormReady,
}) => {
  const sensitivityPCRInput = useFormInput(sensitivityPCR, null, true);
  const sensitivityRDTInput = useFormInput(sensitivityRDT, null, true);
  const specificityPCRInput = useFormInput(specificityPCR, null, true);
  const specificityRDTInput = useFormInput(specificityRDT, null, true);
  const numTestsPCRInput = useFormInput(numTestsPCR, null, true);
  const numTestsRDTInput = useFormInput(numTestsRDT, null, true);

  const [scenariosValue, setScenariosValue] = React.useState({ scenarios });
  // Reset default if url changes
  React.useEffect(() => {
    setScenariosValue({ scenarios });
  }, [scenarios]);

  const handleSubmit = e => {
    e.preventDefault();
    setTestsFormReady(e.target.checkValidity());
    onSubmit &&
      onSubmit({
        sensitivityPCR: sensitivityPCRInput.value,
        sensitivityRDT: sensitivityRDTInput.value,
        specificityPCR: specificityPCRInput.value,
        specificityRDT: specificityRDTInput.value,
        numTestsPCR: numTestsPCRInput.value,
        numTestsRDT: numTestsRDTInput.value,
        scenarios,
      });
  };

  const handleChange = () => {
    setTestsFormReady(false);
  };

  return (
    <section>
      <div className="test-selector action-box">
        <form
          className="tests-form"
          id="tests-form"
          onSubmit={handleSubmit}
          onChange={handleChange}
        >
          <div className="title">
            <div className="number">
              <span>2</span>
            </div>
            <h2 className="underline">
              Define <em>Intervention Scenarios</em>
            </h2>
          </div>
          <ScenarioEditor
            scenarios={scenariosValue.scenarios}
            onSubmit={setScenariosValue}
          />
          <div style={{ width: '100%', margin: '0 auto', textAlign: 'center' }}>
            <div className="submit-button">
              <button className="action submit-button" type="submit">
                See Scenarios
              </button>
            </div>
          </div>
        </form>
      </div>
      <div className="triangle"></div>
    </section>
  );
};

export default TestSelector;
