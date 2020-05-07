import * as React from 'react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';
import {
  IoIosAddCircleOutline,
  IoIosRemoveCircleOutline,
  IoIosInformationCircleOutline,
  IoIosClose,
  IoIosAdd,
} from 'react-icons/io';
import Select from 'react-select';
import Color from 'color';

import { Scenario, InterventionType, InterventionTiming } from '../../API';
import { toLetters } from '../SimulationResults';
import useFormInput, {
  useCheckbox,
  useSelectInput,
  useTextInput,
} from '../../hooks/useFormInput';

import './scenario-editor.less';
import colors from '../../colors';
import ReactTooltip from 'react-tooltip';

const MAX_SCENARIOS = 3;

const ScenarioEditor: React.FC<{
  scenario: Scenario;
  onSubmit?: (scenario: Scenario) => void;
}> = ({ scenario, onSubmit }) => {
  const name = useTextInput(scenario.name, null, true);
  const interventionType = useSelectInput(
    scenario.interventionType,
    null,
    true,
  );
  const description = useTextInput(scenario.description, null, true);
  const interventionTiming = useSelectInput(
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
  const testNumberValidity = () => {
    const cumulative = Array.from(
      document.querySelectorAll<HTMLInputElement>('.proportion-test'),
    ).reduce((memo, element) => {
      const cumulative = (Number(element.value) || 0) + memo;
      const devalidify = () => {
        document
          .querySelectorAll<HTMLInputElement>('.proportion-test')
          .forEach(element => {
            element.setCustomValidity('');
          });
        element.removeEventListener('input', devalidify);
      };
      if (cumulative > 100) {
        element.setCustomValidity('Proportions must not exceed 100');
        element.addEventListener('input', devalidify);
      }
      return cumulative;
    }, 0);
    return cumulative > 100;
  };

  const handleSubmit = e => {
    if (testNumberValidity()) {
      return;
    }

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
      });
  };

  const interventionTypes = [
    { value: InterventionType.LOCKDOWN, label: 'Lockdown' },
    { value: InterventionType.MILD, label: 'Mild' },
    { value: InterventionType.NONE, label: 'None' },
  ];

  const interventionTimings = [
    { value: InterventionTiming.NEVER, label: 'Never' },
    { value: InterventionTiming.VERY_EARLY, label: 'Very early' },
    { value: InterventionTiming.EARLY, label: 'Early' },
    { value: InterventionTiming.LATE, label: 'Late' },
    { value: InterventionTiming.VERY_LATE, label: 'Very late' },
  ];

  return (
    <form id={`scenario-editor-${scenario.name}`} onSubmit={handleSubmit}>
      <div className="form-column">
        <label>Name</label>
        <input {...name} type="text" required />
        <label>description</label>
        <textarea {...description} />

        <a data-tip data-for="interventionType-tooltip">
          <label>
            Intervention Type <IoIosInformationCircleOutline />
          </label>
        </a>
        <ReactTooltip id="interventionType-tooltip">
          {interventionType.value === InterventionType.LOCKDOWN && (
            <p>
              Lockdown consists of severe government-imposed measures similar to
              those taken in China, Italy or Spain. Lockdown implies closure of
              schools and non-essential shops, mandatory work from home whenever
              possible, strong restrictions on movement outside the home, the
              banning of public gatherings (religious ceremonies, sports events,
              concerts etc.) and other similar measures. The goal is to reduce
              R0 – the basic reproductive number – significantly below 1.
            </p>
          )}
          {interventionType.value === InterventionType.MILD && (
            <p>
              Mild intervention consists of a mix of mandatory and voluntary
              measures to achieve social distancing, such as those introduced in
              Sweden. The goal is to reduce R0 – the basic reproductive number –
              to around 1, preventing explosive growth in cases, while limiting
              the economic impact of the measures.
            </p>
          )}
        </ReactTooltip>

        <Select
          onChange={interventionType.onChange}
          options={interventionTypes}
          value={interventionTypes.find(
            ({ value }) => value === interventionType.value,
          )}
          // @ts-ignore
          theme={theme => ({
            ...theme,
            borderRadius: '10px',
            colors: {
              ...theme.colors,
              primary25: Color(colors.turqouise)
                .alpha(0.25)
                .toString(),
              primary: colors.turqouise,
            },
          })}
          styles={{
            valueContainer: defaults => ({
              ...defaults,
              height: '39px',
            }),
            container: defaults => ({
              ...defaults,
              margin: '5px 0 10px 0',
            }),
          }}
        />
        <a data-tip data-for="interventionTimings-tooltip">
          <label>
            Number of deaths before intervention{' '}
            <IoIosInformationCircleOutline />
          </label>
        </a>
        <ReactTooltip id="interventionTimings-tooltip">
          <p>
            This number is an indication of the timing of the intervention. The
            lower the number of deaths before the intervention begins, the
            faster the intervention.
          </p>
        </ReactTooltip>
        <Select
          value={interventionTimings.find(
            ({ value }) => value === interventionTiming.value,
          )}
          onChange={interventionTiming.onChange}
          options={interventionTimings}
          // @ts-ignore
          theme={theme => ({
            ...theme,
            borderRadius: '10px',
            colors: {
              ...theme.colors,
              primary25: Color(colors.turqouise)
                .alpha(0.25)
                .toString(),
              primary: colors.turqouise,
            },
          })}
          styles={{
            valueContainer: defaults => ({
              ...defaults,
              height: '39px',
            }),
            container: defaults => ({
              ...defaults,
              margin: '5px 0 10px 0',
            }),
          }}
        />
        <a data-tip data-for="testSymptomaticOnly-tooltip">
          <label>
            Test Symptomatic Only? <IoIosInformationCircleOutline />
          </label>
        </a>
        <ReactTooltip id="testSymptomaticOnly-tooltip">
          <p>
            With this commonly adopted strategy, only individuals already
            showing COVID-19-like symptoms are tested. Alternatively, tests are
            offered to everyone in a particular sub-population.
          </p>
        </ReactTooltip>
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
          className="proportion-test"
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
          className="proportion-test"
          {...otherHighContactPopulationTestProportion}
          min="0"
          max="100"
          type="number"
          required
        />
        <button type="submit">Enter</button>
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
        interventionTiming: InterventionTiming.LATE,
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
