import * as React from 'react';
import moment from 'moment';
import { ClientSimulationRequest } from '../../types/simulation';
import baseLine from '../../test-scenario.json';

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
            //      .subtract(20, 'days')
                  .format('YYYY-MM-DD')
              : moment()
                  .add(15, 'days')
                  .format('YYYY-MM-DD'),
        })),
      })),
    });
  };

  return (
    <div>
      <button onClick={handleLoadClick}>Load Test Scenario</button>
    </div>
  );
};

export default LoadBaselineScenarioButton;
