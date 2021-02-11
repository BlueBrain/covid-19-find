import * as React from 'react';
import moment from 'moment';
import { ClientSimulationRequest } from '../../types/simulation';
import baseLine from '../../baseline-scenario.json';

const LoadBaselineScenarioButton: React.FC<{
  onLoad: (state: ClientSimulationRequest) => void;
}> = ({ onLoad }) => {
  const handleLoadClick = () => {
    onLoad({
      ...baseLine,
      // @ts-ignore
      scenarios: baseLine.scenarios.map(scenario => ({
        ...scenario,
        phases: scenario.phases.map((phase, index) => ({
          ...phase,
          trigger:
            index === 0
              ? moment()
                  .subtract(34, 'days')
                  .format('YYYY-MM-DD')
              : moment().format('YYYY-MM-DD'),
        })),
      })),
    });
  };

  return (
    <div>
      <button onClick={handleLoadClick}>Load Baseline Scenario</button>
    </div>
  );
};

export default LoadBaselineScenarioButton;
