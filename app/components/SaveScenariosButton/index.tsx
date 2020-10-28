import * as React from 'react';
import { ClientSimulationRequest } from '../../types/simulation';
import { save } from '../../libs/stateLoader';

const SaveScenariosButton: React.FC<{
  state: ClientSimulationRequest;
}> = ({ state }) => {
  const handleSave = () => {
    save(state);
  };

  return (
    <div>
      <button onClick={handleSave}>Save Scenarios</button>
    </div>
  );
};

export default SaveScenariosButton;
