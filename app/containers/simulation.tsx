import * as React from 'react';
import useAPI from '../hooks/useAPI';
import SimulationResults from '../components/SimulationResults';
import { SimulationParams, Scenarios } from '../API';

const Simulation: React.FC<{ simulationParams?: SimulationParams }> = ({
  simulationParams,
}) => {
  const api = useAPI();
  const [simulationData, setSimulationData] = React.useState<{
    loading: boolean;
    error: Error | null;
    data: Scenarios | null;
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

  return <SimulationResults {...simulationData} />;
};

export default Simulation;
