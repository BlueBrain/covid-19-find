import * as React from 'react';

import useAPI from '../hooks/useAPI';
import SimulationResultsComponent from '../components/SimulationResults';
import {
  ClientSimulationRequest,
  SimulationResults,
} from '../types/simulation';
import { CovidData } from '../components/CovidResults';

const Simulation: React.FC<{
  countryData: CovidData;
  clientSimulationRequest?: ClientSimulationRequest;
  ready: boolean;
}> = ({ clientSimulationRequest, countryData, ready }) => {
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
    if (!clientSimulationRequest || !ready) {
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
      ready={ready}
      loading={loading}
      error={error}
      simulationResults={data}
      countryData={countryData}
      clientScenariosInput={clientSimulationRequest.scenarios || []}
    />
  );
};

export default Simulation;
