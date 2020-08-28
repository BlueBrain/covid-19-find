import * as React from 'react';
import useAPI from '../hooks/useAPI';
import SimulationResultsComponent from '../components/SimulationResults';
import { SimulationRequest, SimulationResults } from '../types/simulation';

const Simulation: React.FC<{ simulationParams?: SimulationRequest }> = ({
  simulationParams,
}) => {
  const api = useAPI();
  const [simulationData, setSimulationData] = React.useState<{
    loading: boolean;
    error: Error | null;
    data: SimulationResults | null;
  }>({
    loading: false,
    error: null,
    data: null,
  });

  React.useEffect(() => {
    if (!simulationParams) {
      return;
    }
    setSimulationData({
      loading: true,
      error: null,
      data: null,
    });
    api
      .simulation(simulationParams)
      .then(simulationData => {
        setSimulationData({
          error: null,
          loading: false,
          data: simulationData,
        });
      })
      .catch(error => {
        setSimulationData({
          error,
          loading: false,
          data: null,
        });
      });
  }, [simulationParams]);

  return (
    <SimulationResultsComponent
      {...simulationData}
      scenarios={simulationParams.scenarios}
    />
  );
};

export default Simulation;
