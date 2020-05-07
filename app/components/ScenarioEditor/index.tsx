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
import Switch from 'react-switch';

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
  onChange?: (scenario: Scenario) => void;
  disabled: boolean;
}> = ({ scenario, onChange, disabled }) => {
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
  const scenarioFormId = `#scenario-editor-${scenario.name
    .split(' ')
    .join('-')}`;
  const testNumberValidity = () => {
    const cumulative = Array.from(
      document.querySelectorAll<HTMLInputElement>(
        `${scenarioFormId} .proportion-test`,
      ),
    ).reduce((memo, element) => {
      const cumulative = (Number(element.value) || 0) + memo;
      const devalidify = () => {
        document
          .querySelectorAll<HTMLInputElement>(
            `${scenarioFormId} .proportion-test`,
          )
          .forEach(element => {
            element.setCustomValidity('');
          });
        element.removeEventListener('input', devalidify);
      };
      if (cumulative > 100) {
        element.setCustomValidity('Proportions must be less than 100');
        element.addEventListener('input', devalidify);
      }
      return cumulative;
    }, 0);

    return cumulative === 100;
  };

  const handleBlur = () => {
    if (testNumberValidity()) {
      return;
    }

    onChange &&
      onChange({
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
    { value: InterventionTiming.NEVER, label: 'never' },
    { value: InterventionTiming.GT1, label: '>1' },
    { value: InterventionTiming.GT5, label: '>5' },
    { value: InterventionTiming.GT10, label: '>10' },
    { value: InterventionTiming.GT20, label: '>20' },
    { value: InterventionTiming.GT50, label: '>50' },
  ];

  return (
    <div className="scenario" id={scenarioFormId}>
      <div className="form-column">
        <label>
          <br />
          Name
        </label>
        <input
          {...name}
          type="text"
          required
          disabled={disabled}
          onBlur={handleBlur}
        />
        <label>
          <br />
          description
        </label>
        <textarea {...description} disabled={disabled} onBlur={handleBlur} />
      </div>
      <div className="form-column">
        <a data-tip data-for="interventionType-tooltip">
          <label>
            Intervention Type <IoIosInformationCircleOutline />
          </label>
        </a>
        <ReactTooltip id="interventionType-tooltip">
          {interventionType.value === InterventionType.NONE && (
            <p>
              This option allows you to specify the type of government
              government intervention.Lockdown implies severe government-imposed
              measures similar to those taken in China, Italy or Spain: closure
              of schools and non-essential shops, mandatory work from home
              whenever possible, strong restrictions on movement outside the
              home, the banning of public gatherings (religious ceremonies,
              sports events, concerts etc.) and other similar measures. The goal
              is to reduce R0 – the basic reproductive number – significantly
              below 1. Mild intervention consists of a mix of mandatory and
              voluntary measures to achieve social distancing, such as those
              introduced in Sweden. The goal is to reduce R0 – the basic
              reproductive number – to around 1, preventing explosive growth in
              cases, while limiting the economic impact of the measures.
            </p>
          )}
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
          isDisabled={disabled}
          onChange={interventionType.onChange}
          onBlur={handleBlur}
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
            Start of government intervention <IoIosInformationCircleOutline />
          </label>
        </a>
        <ReactTooltip id="interventionTimings-tooltip">
          <p>
            This option allows you to specify how quickly the government put in
            place measures to contain or suppress the epidemic. The timing of
            government intervention has a major effect on the dynamics of the
            epidemic.
          </p>
        </ReactTooltip>
        <Select
          isDisabled={disabled}
          value={interventionTimings.find(
            ({ value }) => value === interventionTiming.value,
          )}
          onChange={interventionTiming.onChange}
          onBlur={handleBlur}
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
        <div style={{ textAlign: 'left', marginTop: '5px' }}>
          <Switch
            onChange={value => {
              testSymptomaticOnly.onChange(value);
              handleBlur();
            }}
            checked={testSymptomaticOnly.value}
            onColor={colors.turqouise}
            offColor={'#c3c9cc'}
            disabled={disabled}
          />
        </div>
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
          onBlur={handleBlur}
          disabled={disabled}
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
          onBlur={handleBlur}
          disabled={disabled}
        />
      </div>
    </div>
  );
};

const ScenarioList: React.FC<{
  scenarios: Scenario[];
  onSubmit?: (scenarioListSubmit: { scenarios: Scenario[] }) => void;
}> = ({ scenarios = [], onSubmit }) => {
  const [visible, setVisible] = React.useState(false);

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
      onSubmit({
        scenarios: newScenarios,
      });
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
                  <Tab key={`tab-${scenario.name}-${index}`}>
                    {`Scenario ${toLetters(index + 1).toLocaleUpperCase()}`}{' '}
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
      )}
    </div>
  );
};

export default ScenarioList;
