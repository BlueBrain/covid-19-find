import * as React from 'react';

import useAPI from '../hooks/useAPI';
import SimulationResultsComponent from '../components/SimulationResults';
import {
  ClientSimulationRequest,
  SimulationResults,
} from '../types/simulation';

const Simulation: React.FC<{
  clientSimulationRequest?: ClientSimulationRequest;
}> = ({ clientSimulationRequest }) => {
  const api = useAPI();
  const [{ loading, error, data }, setSimulationData] = React.useState<{
    loading: boolean;
    error: Error | null;
    data: SimulationResults | null;
  }>({
    loading: false,
    error: null,
    data: null,
  });

  React.useEffect(() => {
    if (!clientSimulationRequest) {
      return;
    }
    setSimulationData({
      loading: true,
      error: null,
      data: null,
    });
    api
      .simulation(clientSimulationRequest)
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
  }, [clientSimulationRequest]);

  return (
    <SimulationResultsComponent
      loading={loading}
      error={error}
      simulationResults={data}
      clientScenariosInput={clientSimulationRequest.scenarios || []}
    />
  );
};

export default Simulation;
