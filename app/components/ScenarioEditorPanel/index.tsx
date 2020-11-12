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
  scenarioDateTriggers.forEach(triggerPhaseInputList => {
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
          phaseInput.triggerInput.setCustomValidity(
            isAfter
              ? ''
              : `this date must come after ${previousPhaseTriggerValue}`,
          );
        }
      });
  });
  // get only the input list attributes we want
  // form.querySelectorAll("input[data-key="trigger"])
  // split inputs into phases
  // for each phase list, find if the value for trigger is a date
  // if so, the they must be higher than the last phase
};

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
  const formRef = React.useRef();
  // Reset default if url changes
  React.useEffect(() => {
    setScenariosValue({ scenarios });
  }, [scenarios]);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    validateFormWithCustomRules(
      e.target as HTMLFormElement,
      scenariosValue.scenarios,
    );
    setTestsFormReady((e.target as HTMLFormElement).checkValidity());
    onSubmit && onSubmit(scenariosValue);
  };

  const handleChange = () => {
    setTestsFormReady(false);
  };

  const handleFormSubmitButtonClicked = e => {
    formRef.current &&
      validateFormWithCustomRules(formRef.current, scenariosValue.scenarios);
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
