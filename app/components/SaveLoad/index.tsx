import * as React from 'react';
import { ClientSimulationRequest } from '../../types/simulation';
import { save, load } from '../../libs/stateLoader';

const SaveLoadButtons: React.FC<{
  state: ClientSimulationRequest;
  onLoad: (state: ClientSimulationRequest) => void;
}> = ({ state, onLoad }) => {
  const inputRef = React.useRef(null);

  const handleSave = () => {
    save(state);
  };

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
      <button onClick={handleSave}>Save</button>
      <input
        type="file"
        style={{ display: 'none' }}
        ref={inputRef}
        onChange={handleLoad}
      />{' '}
      <button onClick={handleLoadClick}>Load</button>
    </div>
  );
};

export default SaveLoadButtons;
