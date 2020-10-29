import * as React from 'react';
import { ClientSimulationRequest } from '../../types/simulation';
import { load } from '../../libs/stateLoader';

const LoadScenariosButton: React.FC<{
  onLoad: (state: ClientSimulationRequest) => void;
}> = ({ onLoad }) => {
  const inputRef = React.useRef(null);

  const handleLoadClick = () => {
    inputRef.current.click();
  };

  const handleLoad = async e => {
    const state = await load(e as Event);
    if (state) {
      onLoad(state);
    }
  };

  return (
    <div>
      <input
        type="file"
        style={{ display: 'none' }}
        ref={inputRef}
        onChange={handleLoad}
      />{' '}
      <button onClick={handleLoadClick}>Load Scenarios</button>
    </div>
  );
};

export default LoadScenariosButton;
