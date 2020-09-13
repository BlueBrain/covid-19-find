import * as React from 'react';

import ScenarioEditor from '../ScenarioEditor/ScenarioList';
import { ClientScenarioData } from '../../types/simulation';

import './test-selector.less';

const ScenarioEditorPanel: React.FC<{
  defaultScenarios: ClientScenarioData[];
  scenarios: ClientScenarioData[];
  onSubmit?: (props: { scenarios: ClientScenarioData[] }) => void;
  testsFormReady: boolean;
  setTestsFormReady: (value: boolean) => void;
}> = ({
  defaultScenarios,
  scenarios,
  onSubmit,
  testsFormReady,
  setTestsFormReady,
}) => {
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
            defaultScenarios={defaultScenarios}
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

export default ScenarioEditorPanel;
