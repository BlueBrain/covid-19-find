import * as React from 'react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import { IoIosClose, IoIosAdd } from 'react-icons/io';

import ScenarioEditor from './ScenarioEditor';
import { ClientScenarioData } from '../../types/simulation';
import { toLetters } from '../../libs/strings';

import 'react-tabs/style/react-tabs.css';
import './scenario-editor.less';
import { DEFAULT_SCENARIO_LIST } from '../../defaults';

const MAX_SCENARIOS = 3;

const ScenarioList: React.FC<{
  defaultScenarios: ClientScenarioData[];
  scenarios: ClientScenarioData[];
  onSubmit?: (scenarioListSubmit: { scenarios: ClientScenarioData[] }) => void;
}> = ({ defaultScenarios, scenarios = [], onSubmit }) => {
  const removeScenario = (index: number) => e => {
    const newScenarios = [...scenarios].filter((scenario, i) => i !== index);
    onSubmit &&
      onSubmit({
        scenarios: newScenarios,
      });
  };

  const addScenario = () => {
    const newScenarios = [
      ...scenarios,
      {
        ...defaultScenarios[0],
        name: 'New Scenario',
      },
    ];
    onSubmit &&
      onSubmit({
        scenarios: newScenarios,
      });
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
                    <span className="clickable" onClick={removeScenario(index)}>
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
                  defaultPhase={{
                    ...defaultScenarios[0].phases[0],
                    triggerType: null,
                    triggerCondition: null,
                    trigger: null,
                  }}
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
