import * as React from 'react';
import { IoIosClose } from 'react-icons/io';

import { useTextInput } from '../../hooks/useFormInput';
import {
  ClientScenarioData,
  ClientPhase,
  TRIGGER_TYPE,
} from '../../types/simulation';
import PhaseInput from './PhaseInput';
import phaseForm, { AnyInputProp, INPUT_TYPES } from './phaseForm';
import {
  replaceAtIndexWithoutMutation,
  removeAtIndexWithoutMutation,
} from '../../libs/arrays';

import './scenario-editor.less';
import { MAX_PHASE_COUNT } from '../../config';
import TooltipLabel from '../TooltipLabel';

const ScenarioEditor: React.FC<{
  scenario: ClientScenarioData;
  defaultPhase: ClientPhase;
  onChange?: (scenario: ClientScenarioData) => void;
  disabled: boolean;
  scenarioIndex: number;
}> = ({ defaultPhase, scenario, onChange, disabled, scenarioIndex }) => {
  const name = useTextInput(scenario.name, null, true);
  const { phases } = scenario;

  const scenarioFormId = `#scenario-editor-${scenarioIndex}-${scenario.name
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

  const handleAddPhase = () => {
    onChange &&
      onChange({
        name: name.value,
        phases: [
          ...phases,
          {
            ...defaultPhase,
            name: 'New Phase',
          },
        ],
      });
  };

  const handleRemovePhase = (index: number) => () => {
    onChange &&
      onChange({
        name: name.value,
        phases: removeAtIndexWithoutMutation(phases, index),
      });
  };

  return (
    <div className="scenario" id={scenarioFormId}>
      <div className="form-column columns">
        <div>
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
        <div>
          {phases.length < MAX_PHASE_COUNT && (
            <button type="button" onClick={handleAddPhase}>
              Add Phase
            </button>
          )}
        </div>
      </div>
      <div className="columns">
        <div className="col">
          <h2>Phases</h2>
        </div>

        {phases.map((phase, index) => {
          return (
            <div className="col" key={phase.name}>
              <h2 style={{ whiteSpace: 'nowrap' }}>
                {phase.name}
                <span className="clickable" onClick={handleRemovePhase(index)}>
                  <IoIosClose />
                </span>
              </h2>
            </div>
          );
        })}
      </div>
      {phases.length >= 1 ? (
        phaseForm.map((formSection, formSectionIndex) => {
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
                      <div className="col">
                        <TooltipLabel
                          label={input.label}
                          tooltipKey={input.key}
                        ></TooltipLabel>
                      </div>
                      {phases.map((phase, phaseIndex) => {
                        // change type of trigger for validation
                        if (
                          input.key === 'trigger' &&
                          phase.triggerType === TRIGGER_TYPE.DATE
                        ) {
                          // @ts-ignore
                          input.type = INPUT_TYPES.text;
                        }

                        if (
                          input.key === 'trigger' &&
                          phase.triggerType !== TRIGGER_TYPE.DATE
                        ) {
                          input.type = INPUT_TYPES.number;
                        }

                        return (
                          <div
                            className="col"
                            key={`${phase.name}-${input.label}-${phaseIndex}`}
                          >
                            <PhaseInput
                              inputProps={{
                                ...input,
                                name: `${scenarioIndex}-${phaseIndex}-${input.key}-${phase.name}`,
                              }}
                              onChange={handlePhaseChange(input, phaseIndex)}
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
        })
      ) : (
        <div>
          <p style={{ padding: '4em', textAlign: 'center', color: 'white' }}>
            No phases in this scenario
          </p>
        </div>
      )}
    </div>
  );
};

export default ScenarioEditor;
