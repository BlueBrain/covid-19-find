import * as React from 'react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';
import {
  IoIosAddCircleOutline,
  IoIosRemoveCircleOutline,
  IoIosClose,
  IoIosAdd,
} from 'react-icons/io';

import { Scenario } from '../../API';
import { toLetters } from '../SimulationResults';
import useFormInput, {
  useCheckbox,
  useTextInput,
} from '../../hooks/useFormInput';

import './scenario-editor.less';

const ScenarioEditor: React.FC<{
  scenario: Scenario;
  onSubmit?: (scenario: Scenario) => void;
}> = ({ scenario, onSubmit }) => {
  const name = useTextInput(scenario.name, null, true);
  const interventionType = useFormInput(scenario.interventionType, null, true);
  const description = useTextInput(scenario.description, null, true);
  const interventionTiming = useFormInput(
    scenario.interventionTiming,
    null,
    true,
  );
  const testSymptomaticOnly = useCheckbox(
    scenario.testSymptomaticOnly,
    null,
    true,
  );
  const hospitalTestProportion = useFormInput(
    scenario.hospitalTestProportion,
    null,
    true,
  );
  const otherHighContactPopulationTestProportion = useFormInput(
    scenario.otherHighContactPopulationTestProportion,
    null,
    true,
  );
  const restOfPopulationTestProportion = useFormInput(
    scenario.restOfPopulationTestProportion,
    null,
    true,
  );

  const handleSubmit = e => {
    e.preventDefault();
    e.target.dataset.dirty = true;
    onSubmit &&
      onSubmit({
        name: name.value,
        interventionType: interventionType.value,
        description: description.value,
        interventionTiming: interventionTiming.value,
        testSymptomaticOnly: testSymptomaticOnly.value,
        hospitalTestProportion: hospitalTestProportion.value,
        otherHighContactPopulationTestProportion:
          otherHighContactPopulationTestProportion.value,
        restOfPopulationTestProportion: restOfPopulationTestProportion.value,
      });
  };

  return (
    <form id={`scenario-editor-${scenario.name}`} onSubmit={handleSubmit}>
      <div className="form-column">
        <label>Name</label>
        <input {...name} type="text" required />
        <label>description</label>
        <textarea {...description} />
        <label>Test Symptomatic Only?</label>
        <input
          onChange={testSymptomaticOnly.onChange}
          checked={testSymptomaticOnly.value}
          type="checkbox"
        />
      </div>
      <div className="form-column">
        <label>
          Proportion of tests for
          <br />
          hospital staff
        </label>
        <input
          {...hospitalTestProportion}
          min="0"
          max="100"
          type="number"
          required
        />
        <label>
          Proportion of tests for other
          <br />
          highly exposed groups
        </label>
        <input
          {...otherHighContactPopulationTestProportion}
          min="0"
          max="100"
          type="number"
          required
        />
        <label>
          Proportion of tests for
          <br />
          rest of population
        </label>
        <input
          {...restOfPopulationTestProportion}
          min="0"
          max="100"
          type="number"
          required
        />
        <button type="submit">Save</button>
      </div>
    </form>
  );
};

const ScenarioList: React.FC<{
  scenarios: Scenario[];
  onSubmit?: (scenarioListSubmit: { scenarios: Scenario[] }) => void;
}> = ({ scenarios = [], onSubmit }) => {
  const [visible, setVisible] = React.useState(false);

  // const removeScenario = (index: number) => e => {
  //   const newScenarios = [...scenarios].filter((scenario, i) => i !== index);
  //   onSubmit &&
  //     onSubmit({
  //       scenarios: newScenarios,
  //     });
  // };

  return (
    <div className="scenario-editor">
      <h3 className="collapse" onClick={() => setVisible(!visible)}>
        {visible ? <IoIosRemoveCircleOutline /> : <IoIosAddCircleOutline />}{' '}
        Advanced parameters
      </h3>
      {visible && (
        <div className="scenario-list">
          <Tabs>
            <TabList>
              {scenarios.map((scenario, index) => {
                return (
                  <Tab>
                    {`Scenario ${toLetters(index + 1).toLocaleUpperCase()}`}{' '}
                    {/* <button type="button" onClick={removeScenario(index)}>
                      <IoIosClose />
                    </button> */}
                  </Tab>
                );
              })}
            </TabList>
            {scenarios.map((scenario, index) => {
              const handleSubmit = changedScenario => {
                const newScenarios = scenarios;
                newScenarios[index] = changedScenario;
                onSubmit && onSubmit({ scenarios: newScenarios });
              };

              return (
                <TabPanel>
                  <ScenarioEditor scenario={scenario} onSubmit={handleSubmit} />
                </TabPanel>
              );
            })}
          </Tabs>
        </div>
      )}
    </div>
  );
};

export default ScenarioList;
