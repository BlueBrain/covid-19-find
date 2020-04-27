import * as React from 'react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';
import {
  IoIosAddCircleOutline,
  IoIosRemoveCircleOutline,
  IoIosClose,
  IoIosAdd,
} from 'react-icons/io';

import { Scenario, InterventionType, InterventionTiming } from '../../API';
import { toLetters } from '../SimulationResults';
import useFormInput, {
  useCheckbox,
  useTextInput,
} from '../../hooks/useFormInput';

import './scenario-editor.less';

const MAX_SCENARIOS = 3;

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

  const interventionTypes = [
    { value: InterventionType.LOCKDOWN, label: 'Lockdown' },
    { value: InterventionType.MILD, label: 'Mild' },
    { value: InterventionType.NONE, label: 'None' },
  ];

  const interventionTimings = [
    { value: InterventionTiming.NEVER, label: 'never' },
    { value: InterventionTiming.GT10, label: '>10' },
    { value: InterventionTiming.GT50, label: '>50' },
    { value: InterventionTiming.GT500, label: '>500' },
  ];

  return (
    <form id={`scenario-editor-${scenario.name}`} onSubmit={handleSubmit}>
      <div className="form-column">
        <label>Name</label>
        <input {...name} type="text" required />
        <label>description</label>
        <textarea {...description} />
        <label>Intervention Type</label>
        <select onChange={interventionType.onChange}>
          {interventionTypes.map(({ value, label }) => {
            return (
              <option value={value} selected={interventionType.value === value}>
                {label}
              </option>
            );
          })}
        </select>
        <label>Number of deaths before intervention</label>
        <select onChange={interventionTiming.onChange}>
          {interventionTimings.map(({ value, label }) => {
            return (
              <option
                value={value}
                selected={interventionTiming.value === value}
              >
                {label}
              </option>
            );
          })}
        </select>
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
        <button type="submit">Submit</button>
      </div>
    </form>
  );
};

const ScenarioList: React.FC<{
  scenarios: Scenario[];
  onSubmit?: (
    scenarioListSubmit: { scenarios: Scenario[] },
    skipScroll: boolean,
  ) => void;
}> = ({ scenarios = [], onSubmit }) => {
  const [visible, setVisible] = React.useState(false);

  const removeScenario = (index: number) => e => {
    const newScenarios = [...scenarios].filter((scenario, i) => i !== index);
    onSubmit &&
      onSubmit(
        {
          scenarios: newScenarios,
        },
        true,
      );
  };

  const addScenario = () => {
    const newScenarios = [
      ...scenarios,
      {
        name: 'New Scenario',
        description: '',
        interventionType: InterventionType.LOCKDOWN,
        interventionTiming: InterventionTiming.GT10,
        testSymptomaticOnly: true,
        hospitalTestProportion: 0,
        otherHighContactPopulationTestProportion: 0,
        restOfPopulationTestProportion: 0,
      },
    ];
    onSubmit &&
      onSubmit(
        {
          scenarios: newScenarios,
        },
        true,
      );
  };

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
                    <button
                      className="small"
                      type="button"
                      onClick={removeScenario(index)}
                    >
                      <IoIosClose />
                    </button>
                  </Tab>
                );
              })}
              {scenarios.length < MAX_SCENARIOS && (
                <button className="small" type="button" onClick={addScenario}>
                  Add Scenario
                  <IoIosAdd />
                </button>
              )}
            </TabList>
            {scenarios.map((scenario, index) => {
              const handleSubmit = changedScenario => {
                const newScenarios = scenarios;
                newScenarios[index] = changedScenario;
                onSubmit && onSubmit({ scenarios: newScenarios }, false);
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
