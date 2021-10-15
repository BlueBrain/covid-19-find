import * as React from 'react';
import { confirmAlert } from 'react-confirm-alert';
import { IoIosClose } from 'react-icons/io';

import { useTextInput } from '../../hooks/useFormInput';
import {
  ClientScenarioData,
  ClientPhase,
  TRIGGER_TYPE,
} from '../../types/simulation';
import PhaseInput from './PhaseInput';
import phaseForm, {
  AnyInputProp,
  INPUT_TYPES,
  NumberInputProp,
} from './phaseForm';
import {
  replaceAtIndexWithoutMutation,
  removeAtIndexWithoutMutation,
} from '../../libs/arrays';
import { MAX_PHASE_COUNT } from '../../config';
import TooltipLabel from '../TooltipLabel';

import 'react-confirm-alert/src/react-confirm-alert.css';
import './scenario-editor.less';
import tooltips from '../../tooltips';

const ScenarioEditor: React.FC<{
  numberOftest?: number;
  scenario: ClientScenarioData;
  defaultPhase: ClientPhase;
  onChange?: (scenario: ClientScenarioData) => void;
  disabled: boolean;
  scenarioIndex: number;
}> = ({
  defaultPhase,
  scenario,
  onChange,
  disabled,
  scenarioIndex,
  numberOftest,
}) => {
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
    const phase = phases[index];
    confirmAlert({
      title: `Delete ${phase.name}`,
      message: 'Are you sure to delete this phase?',
      buttons: [
        {
          label: 'Yes',
          onClick: () => {
            onChange &&
              onChange({
                name: name.value,
                phases: removeAtIndexWithoutMutation(phases, index),
              });
          },
        },
        {
          label: 'No',
          onClick: () => {}, // No op
        },
      ],
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
              {tooltips[formSection.title] ? (
                <TooltipLabel
                  label={formSection.title}
                  tooltipKey={formSection.title}
                  wrapper={({ children }) => <h3>{children}</h3>}
                />
              ) : (
                <h3>{formSection.title}</h3>
              )}
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
                        // TODO refactor as pattern
                        // change type of trigger for validation
                        const inputProps = { ...input };
                        let value = phase[inputProps.key];

                        if (
                          inputProps.key === 'trigger' &&
                          phase.triggerType === TRIGGER_TYPE.DATE
                        ) {
                          // @ts-ignore
                          inputProps.type = INPUT_TYPES.text;
                        }

                        if (
                          inputProps.key === 'trigger' &&
                          phase.triggerType !== TRIGGER_TYPE.DATE
                        ) {
                          inputProps.type = INPUT_TYPES.number;

                          // These trigger types should be percentages
                          // min 0, max 100
                          // https://github.com/BlueBrain/covid-19-find/issues/201
                          if (
                            phase.triggerType === TRIGGER_TYPE.POSITIVES ||
                            phase.triggerType === TRIGGER_TYPE.INCREASE_CASES ||
                            phase.triggerType === TRIGGER_TYPE.INCREASE_DEATHS
                          ) {
                            (inputProps as NumberInputProp).min = 0;
                            (inputProps as NumberInputProp).max = 100;
                            (inputProps as NumberInputProp).step = 1;
                          }
                        }

                        return (
                          <div
                            className="col"
                            key={`${phase.name}-${inputProps.label}-${phaseIndex}`}
                          >
                            <PhaseInput
                              inputProps={{
                                ...inputProps,
                                name: `${scenarioIndex}-${phaseIndex}-${inputProps.key}-${phase.name}`,
                              }}
                              onChange={handlePhaseChange(
                                inputProps,
                                phaseIndex,
                              )}
                              value={value}
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
