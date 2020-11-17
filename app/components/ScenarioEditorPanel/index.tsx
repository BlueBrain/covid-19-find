import * as React from 'react';
import moment from 'moment';

import ScenarioEditor from '../ScenarioEditor/ScenarioList';
import { ClientScenarioData, TRIGGER_TYPE } from '../../types/simulation';

import './test-selector.less';

const validateFormWithCustomRules = (
  form: HTMLFormElement,
  scenarios: ClientScenarioData[],
) => {
  // Here we will validate the form
  // Trigger Dates of each scenario must come after the preceeding date.
  const invalidScenarios = new Set<number>();
  const inputs = Array.from(form.querySelectorAll(`input`));
  const inputsByScenario = inputs.reduce((memo, input) => {
    const [scenarioIndex, phaseIndex, inputKey] = input.name.split('-');
    // do validation here?
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

  const triggers = Array.from(
    form.querySelectorAll(`input[data-key="trigger"]`),
  );
  const scenarioDateTriggers = scenarios.map(({ phases }, scenarioIndex) => {
    return phases.map((phase, phaseIndex) => {
      return {
        triggerType: phase.triggerType,
        triggerInput: triggers[phaseIndex + scenarioIndex] as HTMLInputElement,
        triggerValue: phase.trigger,
      };
    });
  });
  scenarioDateTriggers.forEach((triggerPhaseInputList, scenarioIndex) => {
    // lets check the values from the back
    // we only care about validating dates
    triggerPhaseInputList
      .reverse()
      .filter(({ triggerType }) => triggerType === TRIGGER_TYPE.DATE)
      .forEach((phaseInput, phaseInputIndex) => {
        // the current phase's date value must come later than the previous phase's date value
        const previousPhaseTriggerValue =
          triggerPhaseInputList[phaseInputIndex + 1]?.triggerValue;
        if (previousPhaseTriggerValue) {
          const isAfter = moment(phaseInput.triggerValue).isAfter(
            moment(previousPhaseTriggerValue),
          );
          if (isAfter) {
            phaseInput.triggerInput.setCustomValidity('');
            return;
          }
          phaseInput.triggerInput.setCustomValidity(
            `this date must come after ${previousPhaseTriggerValue}`,
          );
          invalidScenarios.add(scenarioIndex);
        }
      });
  });
  // get only the input list attributes we want
  // form.querySelectorAll("input[data-key="trigger"])
  // split inputs into phases
  // for each phase list, find if the value for trigger is a date
  // if so, the they must be higher than the last phase

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
    setInvalidScenarioIndexes(Array.from(invalidScenarios.keys()).sort());
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    runValidator();
    onSubmit && onSubmit(scenariosValue);
  };

  const handleChange = () => {
    runValidator();
    setTestsFormReady(false);
  };

  const handleFormSubmitButtonClicked = e => {
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
          />
          <div style={{ width: '100%', margin: '0 auto', textAlign: 'center' }}>
            {!isValid && !!invalidScenarioIndexes.length && (
              <div className="error-report">
                <p>
                  There are still errors present in the following scenarios.
                </p>
                <ul>
                  {invalidScenarioIndexes.map(scenarioIndex => {
                    return <li>{scenarios[scenarioIndex].name}</li>;
                  })}
                </ul>
              </div>
            )}
            <div className="submit-button">
              <button
                className="action submit-button"
                type="submit"
                onClick={handleFormSubmitButtonClicked}
              >
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
