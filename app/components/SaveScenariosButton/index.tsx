import * as React from 'react';
import { ClientSimulationRequest } from '../../types/simulation';
import { save } from '../../libs/stateLoader';

const SaveScenariosButton: React.FC<{
  state: ClientSimulationRequest;
  disabled: boolean;
}> = ({ state, disabled }) => {
  const handleSave = () => {
    save(state);
  };

  return (
    <div>
      <button disabled={disabled} onClick={handleSave}>Save Scenarios</button>
    </div>
  );
};

export default SaveScenariosButton;
