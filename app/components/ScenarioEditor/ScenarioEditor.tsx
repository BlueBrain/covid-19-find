import * as React from 'react';

import { Scenario } from '../../API';
import useFormInput, {
  useDirectInput,
  useSelectInput,
  useTextInput,
} from '../../hooks/useFormInput';
import phaseForm from './phaseForm';

import './scenario-editor.less';
import PhaseInput from './PhaseInput';

const ScenarioEditor: React.FC<{
  scenario: Scenario;
  onChange?: (scenario: any) => void;
  disabled: boolean;
}> = ({ scenario, onChange, disabled }) => {
  const phases = [
    {
      name: 'Current Phase',
    },
    {
      name: 'Next Phase',
    },
  ];

  const name = useTextInput(scenario.name, null, true);

  const scenarioFormId = `#scenario-editor-${scenario.name
    .split(' ')
    .join('-')}`;

  const handleBlur = () => {
    onChange &&
      onChange({
        name: name.value,
      });
  };

  return (
    <div className="scenario" id={scenarioFormId}>
      <div className="form-column">
        <label>
          <br />
          Scenario Name
        </label>
        <input
          {...name}
          type="text"
          required
          disabled={disabled}
          onBlur={handleBlur}
        />
      </div>
      <div className="columns">
        <div className="col" style={{ width: 200 }}>
          <h2>Phases</h2>
        </div>
        {phases.map(phase => {
          return (
            <div className="col" style={{ width: 200 }}>
              <h2>{phase.name}</h2>
            </div>
          );
        })}
      </div>
      {phaseForm.map(formSection => {
        return (
          <>
            <hr />
            <h3>{formSection.title}</h3>
            <div className="phase-section">
              {formSection.input.map(input => {
                return (
                  <div className="columns">
                    <div className="col" style={{ width: 200 }}>
                      <label>{input.label}</label>
                    </div>
                    {phases.map(phase => {
                      return (
                        <div className="col" style={{ width: 200 }}>
                          <PhaseInput
                            inputProps={input}
                            onChange={value => {
                              // TODO save changes
                            }}
                          />
                        </div>
                      );
                    })}
                  </div>
                );
              })}
            </div>
          </>
        );
      })}
    </div>
  );
};

export default ScenarioEditor;
