import * as React from 'react';
import moment from 'moment';

import ScenarioEditor from '../ScenarioEditor/ScenarioList';
import { ClientScenarioData, TRIGGER_TYPE } from '../../types/simulation';

import './test-selector.less';

const validateFormWithCustomRules = (
  form: HTMLFormElement,
  scenarios: ClientScenarioData[],
) => {
  const MAX_EARLIEST_DAYS_AGO = 35;
  // Here we will validate the form
  // Trigger Dates of each scenario must come after the preceeding date.
  const invalidScenarios = new Set<number>();
  const inputs = Array.from(form.querySelectorAll(`input`));
  const inputsByScenario = inputs.reduce((memo, input) => {
    const [scenarioIndex, phaseIndex, inputKey] = input.name.split('-');
    // do validation here?

    if (inputKey === 'trigger') {
      // check type
      // get triggerType
      const triggerType =
        scenarios[scenarioIndex]?.phases[phaseIndex].triggerType;
      if (triggerType === TRIGGER_TYPE.DATE) {
        // now we should validate if its a proper date
        const date = moment(input.value);
        input.setCustomValidity(
          date.isValid() ? '' : 'Please enter a valid date',
        );

        // we should also check if the date occurs after
        // any of the previous date values
        const getPreviousDateValue = (phaseIndex: number) => {
          const prevPhase = scenarios[scenarioIndex].phases[phaseIndex - 1];
          if (!prevPhase) {
            return null;
          }
          if (prevPhase.triggerType === TRIGGER_TYPE.DATE) {
            return prevPhase.trigger;
          }
          return getPreviousDateValue(phaseIndex - 2);
        };

        const prevPhaseDateValue = getPreviousDateValue(Number(phaseIndex));
        if (prevPhaseDateValue) {
          const isAfter = date.isAfter(moment(prevPhaseDateValue));
          input.setCustomValidity(
            isAfter ? '' : `this date must come after ${prevPhaseDateValue}`,
          );
        }

        // Users should not be able to enter a date MAX_EARLIEST_DAYS_AGO (35) days before today
        // https://github.com/BlueBrain/covid-19-find/issues/179
        if (
          date.isBefore(
            moment(new Date()).subtract(MAX_EARLIEST_DAYS_AGO + 1, 'days'),
          )
        ) {
          input.setCustomValidity(
            `Please enter a date no earlier than ${MAX_EARLIEST_DAYS_AGO} days in the past`,
          );
        }
      }
    }

    const isValid = input.checkValidity();
    if (!isValid) {
      invalidScenarios.add(Number(scenarioIndex));
    }

    if (!memo[scenarioIndex]) {
      memo[scenarioIndex] = [];
    }

    memo[scenarioIndex].push(input);
    return memo;
  }, invalidScenarios);

  return invalidScenarios;
};

const ScenarioEditorPanel: React.FC<{
  defaultScenarios: ClientScenarioData[];
  scenarios: ClientScenarioData[];
  onSubmit?: (props: { scenarios: ClientScenarioData[] }) => void;
  testsFormReady: boolean;
  setTestsFormReady: (value: boolean) => void;
}> = ({ defaultScenarios, scenarios, onSubmit, setTestsFormReady }) => {
  const [scenariosValue, setScenariosValue] = React.useState({ scenarios });
  const [isValid, setValidity] = React.useState(false);
  const [invalidScenarioIndexes, setInvalidScenarioIndexes] = React.useState<
    number[]
  >([]);
  const formRef = React.useRef<HTMLFormElement>(null);

  // Reset default if url changes
  React.useEffect(() => {
    setScenariosValue({ scenarios });
  }, [scenarios]);

  const runValidator = () => {
    setTestsFormReady((formRef.current as HTMLFormElement).checkValidity());
    setValidity((formRef.current as HTMLFormElement).checkValidity());
    const invalidScenarios = validateFormWithCustomRules(
      formRef.current as HTMLFormElement,
      scenariosValue.scenarios,
    );
    (formRef.current as HTMLFormElement).reportValidity();
    setInvalidScenarioIndexes(Array.from(invalidScenarios.keys()).sort());
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSubmit && onSubmit(scenariosValue);
  };

  const handleChange = () => {
    setTestsFormReady(false);
  };

  const handleSubmitButtonClicked = () => {
    runValidator();
  };

  return (
    <section>
      <div className="test-selector action-box">
        <form
          className="tests-form"
          id="tests-form"
          onSubmit={handleSubmit}
          onChange={handleChange}
          ref={formRef}
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
            onChange={handleChange}
          />
          <div style={{ width: '100%', margin: '0 auto', textAlign: 'center' }}>
            {!isValid && !!invalidScenarioIndexes.length && (
              <div className="error-report">
                <p>
                  There are still errors present in the following scenarios:
                </p>
                <ul>
                  {invalidScenarioIndexes.map(scenarioIndex => {
                    return (
                      <li style={{ marginBottom: '0.5em' }}>
                        {scenarios[scenarioIndex].name}
                      </li>
                    );
                  })}
                </ul>
              </div>
            )}
            <div className="submit-button">
              <button
                className="action submit-button"
                type="submit"
                onClick={handleSubmitButtonClicked}
              >
                See Scenarios For Next Six Months
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
