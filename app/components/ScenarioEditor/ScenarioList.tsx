import * as React from 'react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import { IoIosClose, IoIosAdd } from 'react-icons/io';

import { toLetters } from '../SimulationResults';
import ScenarioEditor from './ScenarioEditor';
import { Scenario, ClientScenarioData } from '../../types/simulation';

import 'react-tabs/style/react-tabs.css';
import './scenario-editor.less';

const MAX_SCENARIOS = 3;

const ScenarioList: React.FC<{
  scenarios: ClientScenarioData[];
  onSubmit?: (scenarioListSubmit: { scenarios: ClientScenarioData[] }) => void;
}> = ({ scenarios = [], onSubmit }) => {
  const removeScenario = (index: number) => e => {
    const newScenarios = [...scenarios].filter((scenario, i) => i !== index);
    onSubmit &&
      onSubmit({
        scenarios: newScenarios,
      });
  };

  const addScenario = () => {
    // TODO add a scenario
    // const newScenarios = [
    //   ...scenarios,
    //   {
    //     name: 'New Scenario',
    //     description: '',
    //     testSymptomaticOnly: true,
    //     hospitalTestProportion: 0,
    //     otherHighContactPopulationTestProportion: 0,
    //     restOfPopulationTestProportion: 0,
    //   },
    // ];
    // onSubmit &&
    //   onSubmit({
    //     scenarios: newScenarios,
    //   });
  };

  return (
    <div className="scenario-editor">
      <div className="scenario-list">
        <Tabs>
          <TabList>
            {scenarios.map((scenario, index) => {
              return (
                <Tab key={`tab-${scenario.name}-${index}`}>
                  {index === 0
                    ? 'Counterfactual: No tests and no intervention'
                    : `Scenario ${toLetters(index).toLocaleUpperCase()}`}{' '}
                  {scenarios.length > 1 && index !== 0 && (
                    <span onClick={removeScenario(index)}>
                      <IoIosClose />
                    </span>
                  )}
                </Tab>
              );
            })}
            {scenarios.length < MAX_SCENARIOS && (
              <a className="add-scenario" onClick={addScenario}>
                Add Scenario
                <IoIosAdd />
              </a>
            )}
          </TabList>
          {scenarios.map((scenario, index) => {
            const handleSubmit = changedScenario => {
              const newScenarios = scenarios;
              newScenarios[index] = changedScenario;
              onSubmit && onSubmit({ scenarios: newScenarios });
            };

            return (
              <TabPanel key={`panel-${scenario.name}-${index}`}>
                <ScenarioEditor
                  scenario={scenario}
                  onChange={handleSubmit}
                  disabled={index === 0}
                />
              </TabPanel>
            );
          })}
        </Tabs>
      </div>
    </div>
  );
};

export default ScenarioList;
