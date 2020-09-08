import * as React from 'react';

import { useTextInput } from '../../hooks/useFormInput';
import { ClientScenarioData, ClientPhase } from '../../types/simulation';
import PhaseInput from './PhaseInput';
import phaseForm, { AnyInputProp } from './phaseForm';
import { replaceAtIndexWithoutMutation } from '../../libs/arrays';

import './scenario-editor.less';

const ScenarioEditor: React.FC<{
  scenario: ClientScenarioData;
  onChange?: (scenario: ClientScenarioData) => void;
  disabled: boolean;
}> = ({ scenario, onChange, disabled }) => {
  const name = useTextInput(scenario.name, null, true);
  const { phases } = scenario;

  const scenarioFormId = `#scenario-editor-${scenario.name
    .split(' ')
    .join('-')}`;

  const handleBlur = () => {
    onChange &&
      onChange({
        name: name.value,
        phases,
      });
  };

  const handlePhaseChange = (input: AnyInputProp, phaseIndex: number) => (
    value: string | number | boolean | null | undefined,
  ) => {
    const phaseToChange = { ...phases[phaseIndex], [input.key]: value };
    onChange &&
      onChange({
        name: name.value,
        phases: replaceAtIndexWithoutMutation<ClientPhase>(
          phases,
          phaseToChange,
          phaseIndex,
        ),
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
            <div className="col" style={{ width: 200 }} key={phase.name}>
              <h2>{phase.name}</h2>
            </div>
          );
        })}
      </div>
      {phaseForm.map((formSection, formSectionIndex) => {
        return (
          <div key={`${formSection.title}-${formSectionIndex}`}>
            <hr />
            <h3>{formSection.title}</h3>
            <div className="phase-section">
              {formSection.input.map((input, formSectionInputIndex) => {
                return (
                  <div
                    className="columns"
                    key={`${formSection.title}-${input.label}-${formSectionInputIndex}`}
                  >
                    <div className="col" style={{ width: 200 }}>
                      <label>{input.label}</label>
                    </div>
                    {phases.map((phase, index) => {
                      return (
                        <div
                          className="col"
                          style={{ width: 200 }}
                          key={`${phase.name}-${input.label}-${index}`}
                        >
                          <PhaseInput
                            inputProps={input}
                            onChange={handlePhaseChange(input, index)}
                            value={phase[input.key]}
                          />
                        </div>
                      );
                    })}
                  </div>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ScenarioEditor;
