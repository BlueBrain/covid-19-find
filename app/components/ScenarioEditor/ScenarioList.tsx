import * as React from 'react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import { IoIosClose, IoIosAdd } from 'react-icons/io';
import { confirmAlert } from 'react-confirm-alert';

import ScenarioEditor from './ScenarioEditor';
import { ClientScenarioData } from '../../types/simulation';
import { MAX_SCENARIOS_COUNT } from '../../config';

import 'react-confirm-alert/src/react-confirm-alert.css';
import 'react-tabs/style/react-tabs.css';
import './scenario-editor.less';

const ScenarioList: React.FC<{
  numberOftest?: number;
  defaultScenarios: ClientScenarioData[];
  scenarios: ClientScenarioData[];
  onSubmit?: (scenarioListSubmit: { scenarios: ClientScenarioData[] }) => void;
  onChange: () => void;
}> = ({
  numberOftest,
  defaultScenarios,
  scenarios = [],
  onSubmit,
  onChange,
}) => {
  const removeScenario = (index: number) => e => {
    const newScenarios = [...scenarios].filter((scenario, i) => i !== index);
    const scenario = scenarios[index];
    confirmAlert({
      title: `Delete Scenario: ${scenario.name}`,
      message: 'Are you sure to delete this scenario?',
      buttons: [
        {
          label: 'Yes',
          onClick: () => {
            onSubmit &&
              onSubmit({
                scenarios: newScenarios,
              });
            onChange();
          },
        },
        {
          label: 'No',
          onClick: () => {}, // No op
        },
      ],
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
    onChange();
  };

  return (
    <div className="scenario-editor">
      <div className="scenario-list">
        <Tabs forceRenderTabPanel={true}>
          <TabList>
            {scenarios.map((scenario, index) => {
              return (
                <Tab
                  key={`tab-${scenario.name}-${index}`}
                  style={{ justifyContent: 'space-between' }}
                >
                  <span className="label">{scenario.name}</span>
                  {scenarios.length > 1 && index !== 0 && (
                    <span className="clickable" onClick={removeScenario(index)}>
                      <IoIosClose />
                    </span>
                  )}
                </Tab>
              );
            })}
            {scenarios.length < MAX_SCENARIOS_COUNT && (
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
              onChange();
            };

            return (
              <TabPanel key={`panel-${scenario.name}-${index}`}>
                <ScenarioEditor
                  numberOftest={numberOftest}
                  defaultPhase={{
                    ...defaultScenarios[0].phases[0],
                    triggerType: null,
                    triggerCondition: null,
                    trigger: null,
                  }}
                  scenarioIndex={index}
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
